# tests/test_validate_schema.py

"""
Test to ensure the OutlookCategoryArray JSON schema is still valid
after changing its representation to an object keyed by UUID.
"""

import json
from pathlib import Path

import jsonschema


def test_outlook_category_array_schema():
    """
    Load the local JSON schema and verify it conforms to JSON Schema Draft 2020-12.
    """
    schema_path = Path(__file__).parent.parent / "schemas" / "OutlookCategoryArray.json"
    with schema_path.open(encoding="utf-8") as f:
        schema = json.load(f)

    # This will raise if the schema itself is invalid
    jsonschema.Draft202012Validator.check_schema(schema)
    print("✅ OutlookCategoryArray.json is a valid Draft 2020-12 schema.")
