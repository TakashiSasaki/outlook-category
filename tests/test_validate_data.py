# tests/test_validate_data.py

import json
import subprocess
import jsonschema
from pathlib import Path
import sys
import pytest

@pytest.fixture(autouse=True)
def skip_on_non_windows():
    if sys.platform != "win32":
        pytest.skip("This test requires PowerShell and Outlook COM, so only runs on Windows")

def test_export_and_validate(tmp_path):
    """
    Run the PowerShell export script and validate its output
    against the OutlookCategories.json schema.
    """
    # Locate project root
    project_root = Path(__file__).parent.parent

    # Paths under project root
    schema_path   = project_root / "schemas" / "OutlookCategories.json"
    data_path     = project_root / "OutlookCategories.json"
    script_path   = project_root / "powershell" / "Export-OutlookCategoriesToJson.ps1"

    # Clean up any existing output file
    if data_path.exists():
        data_path.unlink()

    # Invoke the PowerShell script
    # Use 'pwsh' if PowerShell 7+, otherwise 'powershell'
    pwsh = "pwsh" if subprocess.run(["where", "pwsh"], capture_output=True).returncode == 0 else "powershell"
    result = subprocess.run(
        [pwsh, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path), "-OutputPath", str(data_path)],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Export failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert data_path.exists(), "Expected the export script to write OutlookCategories.json"

    # Load schema and data
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data   = json.loads(data_path.read_text(encoding="utf-8-sig"))

    # Validate JSON structure
    jsonschema.validate(instance=data, schema=schema, cls=jsonschema.Draft202012Validator)
