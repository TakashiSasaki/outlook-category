# tests/test_get_outlook_categories_schema.py

import sys
import json
import pytest
from pathlib import Path
from jsonschema.validators import Draft202012Validator
from referencing import Registry, Resource
from outlook_categories.get_outlook_categories import get_outlook_categories

@pytest.fixture(autouse=True)
def skip_on_non_windows():
    if sys.platform != "win32":
        pytest.skip("Skipping Outlook COM tests on non-Windows platforms")

def test_get_outlook_categories_conforms_to_root_schema():
    """
    Call get_outlook_categories(), then validate its result against
    the OutlookCategories.json schema, resolving $ref locally.
    """
    # 1) Call the function
    result = get_outlook_categories()
    assert isinstance(result, dict), "Expected a dict keyed by schema UUID"
    assert len(result) == 1, "Expected exactly one top-level key"
    schema_uuid = next(iter(result))

    # 2) Load schemas
    project_root     = Path(__file__).parent.parent
    root_schema_path = project_root / "schemas" / "OutlookCategories.json"
    item_schema_path = project_root / "schemas" / "OutlookCategory.json"

    root_schema = json.loads(root_schema_path.read_text(encoding="utf-8"))
    item_schema = json.loads(item_schema_path.read_text(encoding="utf-8"))

    # 3) Extract the $ref under properties[schema_uuid].items
    try:
        ref = root_schema["properties"][schema_uuid]["items"]["$ref"]
    except KeyError:
        pytest.skip("Root schema is not in the expected format")

    # 4) Build a registry and register both schemas under their $id or ref URIs
    registry = Registry().with_resource(
        root_schema["$id"], Resource.from_contents(root_schema)
    ).with_resource(
        ref, Resource.from_contents(item_schema)
    )

    # 5) Validate
    validator = Draft202012Validator(root_schema, registry=registry)  # type: ignore[arg-type]
    validator.validate(result)
