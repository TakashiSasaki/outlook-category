"""
dodo.py – Local health-check task runner

Tasks implemented
------------------
* **lint**            – Run *ruff* and *black --check*
* **validate_schema** – Validate the JSON-Schema (Draft 2020-12) itself
* **export**          – Run the PowerShell export then validate the resulting JSON
* **health**          – Convenience meta-task that executes all checks above
"""

from pathlib import Path
import json
import jsonschema

# Configure doit: run the ``health`` meta-task when no task name is given
DOIT_CONFIG = {
    "default_tasks": ["health"],
}

# ---------- Common paths ----------
SCHEMA_JSON = Path("schemas/OutlookCategoryArray.json")
VALIDATE_DATA = Path("validate_data.py")

# ---------- Task definitions ----------


def task_lint():
    """Static-analysis: ruff lint and black formatting check."""
    return {
        "actions": [
            "poetry run ruff check .",
            "poetry run black --check .",
        ],
        "verbosity": 2,
    }


def task_validate_schema():
    """Validate *OutlookCategoryArray.json* against Draft 2020-12 meta-schema."""

    def _validate():
        with SCHEMA_JSON.open(encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.Draft202012Validator.check_schema(schema)
        print("✅ OutlookCategoryArray.json is a valid Draft-2020-12 schema.")

    return {
        "actions": [_validate],
        "file_dep": [str(SCHEMA_JSON)],
        "verbosity": 2,
    }


def task_export():
    """Run the PowerShell export script and validate the produced JSON."""
    cmd = f"poetry run python {VALIDATE_DATA}"
    return {
        "actions": [cmd],
        "file_dep": [str(VALIDATE_DATA)],
        "verbosity": 2,
    }


def task_health():
    """Meta-task that executes *lint*, *validate_schema* and *export* in sequence."""
    return {
        "actions": None,  # Only dependencies will run
        "task_dep": ["lint", "validate_schema", "export"],
    }

def task_generate_schemas():
    """
    Generate JSON Schemas from Pydantic models and store them under schemas/generated/
    """
    output_dir = Path("schemas/generated")
    return {
        "actions": [
            (output_dir.mkdir, [], {"parents": True, "exist_ok": True}),
            f"poetry run python scripts/print_outlook_category_schema_alias.py > {output_dir / 'OutlookCategory.json'}",
            f"poetry run python scripts/print_outlook_categories_schema.py > {output_dir / 'OutlookCategories.json'}",
        ],
        "targets": [
            output_dir / "OutlookCategory.json",
            output_dir / "OutlookCategories.json",
        ],
        "file_dep": [
            "scripts/print_outlook_category_schema_alias.py",
            "scripts/print_outlook_categories_schema.py",
        ],
        "verbosity": 2,
    }
