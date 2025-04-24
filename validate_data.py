# validate_data.py
"""
Script to export Outlook categories via PowerShell and validate the resulting JSON
against the OutlookCategoryArray.json schema (Draft 2020-12) using jsonschema.
"""

import subprocess
import json
import jsonschema
from pathlib import Path

# JSON-based schema and data file paths
SCHEMA_PATH = Path("schemas/OutlookCategoryArray.json")
DATA_PATH = Path("outlook_categories.json")
EXPORT_SCRIPT = Path("Export-OutlookCategoriesToJson.ps1")


def run_export_script():
    """
    Execute the PowerShell script to export Outlook categories into a JSON file.
    Raises RuntimeError if the script fails.
    """
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(EXPORT_SCRIPT),
            "-OutputPath",
            str(DATA_PATH),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("PowerShell script failed")
    print("[Export] Export completed:", DATA_PATH)


def validate_json():
    """
    Load the JSON schema and exported data, then validate the data against the schema.
    Raises jsonschema.ValidationError on failure.
    """
    # Load the schema JSON file
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    # Load the exported JSON data with BOM-compatible UTF-8 decoding
    with DATA_PATH.open(encoding="utf-8-sig") as f:
        data = json.load(f)
    # Validate the JSON data against the schema
    jsonschema.validate(
        instance=data, schema=schema, cls=jsonschema.Draft202012Validator
    )
    print("✅ JSON data is valid according to OutlookCategoryArray schema.")


def main():
    """
    Run the export and validation sequence.
    """
    run_export_script()
    validate_json()


if __name__ == "__main__":
    main()
