# tests/test_get_outlook_categories.py

import sys
import pytest
from outlook_categories.get_outlook_categories import get_outlook_categories
from outlook_categories.models import OutlookCategory

@pytest.fixture(autouse=True)
def skip_on_non_windows():
    if sys.platform != "win32":
        pytest.skip("Skipping Outlook COM tests on non-Windows platforms")

def test_get_outlook_categories_returns_list():
    cats = get_outlook_categories()
    assert isinstance(cats, list), "Expected a list of categories"
    assert len(cats) > 0, "Expected at least one category"

@pytest.mark.parametrize("item", get_outlook_categories())
def test_each_item_validates_against_model(item):
    # parse_obj will raise ValidationError if any field is wrong
    model = OutlookCategory.parse_obj(item)
    assert isinstance(model, OutlookCategory)
    # Spot-check some fields
    assert isinstance(model.Account, str) and model.Account, "Account must be a non-empty string"
    assert isinstance(model.CategoryID, str) and model.CategoryID.startswith("{") and model.CategoryID.endswith("}")
    assert isinstance(model.Color, int) and 0 <= model.Color <= 25
    assert isinstance(model.Name, str) and model.Name
    assert model.ClassName == "olCategory"
    assert isinstance(model.Application_Name, str) and model.Application_Name
    assert isinstance(model.Application_Version, str) and model.Application_Version
    assert isinstance(model.Session_CurrentUser, str) and model.Session_CurrentUser
    assert isinstance(model.Session_DefaultStore, str) and model.Session_DefaultStore
