# tests/test_get_outlook_categories.py

import sys
import pytest
from outlook_categories.get_outlook_categories import get_outlook_categories, SCHEMA_UUID
from outlook_categories.models import OutlookCategory

@pytest.fixture(autouse=True)
def skip_on_non_windows():
    if sys.platform != "win32":
        pytest.skip("Skipping Outlook COM tests on non-Windows platforms")

def test_get_outlook_categories_returns_dict():
    result = get_outlook_categories()
    # Should be a dict keyed by the schema UUID
    assert isinstance(result, dict), "Expected a dict keyed by schema UUID"
    assert SCHEMA_UUID in result, f"Expected key {SCHEMA_UUID!r} in result"
    items = result[SCHEMA_UUID]
    assert isinstance(items, list), "Expected the value to be a list of categories"
    assert len(items) > 0, "Expected at least one category in the list"

@pytest.mark.parametrize("item", get_outlook_categories().get(SCHEMA_UUID, []))
def test_each_item_validates_against_model(item):
    # model_validate will raise ValidationError if any field is wrong
    model = OutlookCategory.model_validate(item)
    assert isinstance(model, OutlookCategory)
    # Spot-check some fields via alias-based access
    assert isinstance(model.Account, str) and model.Account, "Account must be a non-empty string"
    assert isinstance(model.CategoryID, str) and model.CategoryID.startswith("{") and model.CategoryID.endswith("}")
    assert isinstance(model.Color, int) and 0 <= model.Color <= 25
    assert isinstance(model.Name, str) and model.Name
    assert model.ClassName == "olCategory"
    assert isinstance(model.Application_Name, str) and model.Application_Name
    assert isinstance(model.Application_Version, str) and model.Application_Version
    assert isinstance(model.Session_CurrentUser, str) and model.Session_CurrentUser
    assert isinstance(model.Session_DefaultStore, str) and model.Session_DefaultStore
