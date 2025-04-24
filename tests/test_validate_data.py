# tests/test_validate_data.py

import json
import subprocess
import sys
import pytest
from pathlib import Path
from jsonschema.validators import Draft202012Validator
from referencing import Registry, Resource


@pytest.fixture(autouse=True)
def skip_on_non_windows():
    if sys.platform != "win32":
        pytest.skip("This test requires PowerShell and Outlook COM, so only runs on Windows")


def test_export_and_validate(tmp_path):
    """
    Run the PowerShell export script and validate its output
    against the OutlookCategories.json schema using referencing.Registry
    to resolve $ref locally (no deprecated RefResolver).
    """
    project_root  = Path(__file__).parent.parent
    schema_root   = project_root / "schemas" / "OutlookCategories.json"
    schema_item   = project_root / "schemas" / "OutlookCategory.json"
    data_file     = project_root / "OutlookCategories.json"
    script_path   = project_root / "powershell" / "Export-OutlookCategoriesToJson.ps1"

    # Clean up any old export
    if data_file.exists():
        data_file.unlink()

    # Export via PowerShell
    shell = "pwsh" if subprocess.run(["where", "pwsh"], capture_output=True).returncode == 0 else "powershell"
    result = subprocess.run(
        [shell, "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", str(script_path), "-OutputPath", str(data_file)],
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Export failed:\n{result.stdout}\n{result.stderr}"
    assert data_file.exists(), "Expected OutlookCategories.json to be created"

    # Load schemas & data
    root_schema = json.loads(schema_root.read_text(encoding="utf-8"))
    item_schema = json.loads(schema_item.read_text(encoding="utf-8"))
    data        = json.loads(data_file.read_text(encoding="utf-8-sig"))

    # Build a referencing.Registry and register both schemas by their $id
    # Build a referencing.Registry and register both schemas by their $id
    registry = Registry().with_resource(
        root_schema["$id"],
        Resource.from_contents(root_schema)
    ).with_resource(
        item_schema["$id"],
        Resource.from_contents(item_schema)
    )
    # Also register the JSON‐schema URL (root schema uses this in its $ref)
    # by converting the YAML $id to the JSON filename URL
    json_ref = item_schema["$id"].replace(".yaml", ".json")
    registry = registry.with_resource(
        json_ref,
        Resource.from_contents(item_schema)
    )

    # Validate with Draft202012Validator, passing our registry.
    # (We add a type-ignore to satisfy the Pylance stub.)
    # Validate using our registry (type-ignore silences Pylance stub warning)
    validator = Draft202012Validator(root_schema, registry=registry)  # type: ignore[arg-type]
    validator.validate(data)