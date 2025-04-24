# src/outlook_categories/models.py

from typing import Any, Dict
from pydantic import BaseModel, Field, ConfigDict

class OutlookCategory(BaseModel):
    """
    Pydantic v2 model for an Outlook category, with alias-based attribute access.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    account: str = Field(..., alias="Account")
    category_id: str = Field(..., alias="CategoryID", pattern=r"^\{[0-9A-Fa-f\-]{36}\}$")
    color: int = Field(..., alias="Color", ge=0, le=25)
    name: str = Field(..., alias="Name")
    class_name: str = Field(..., alias="ClassName")
    application_name: str = Field(..., alias="Application.Name")
    application_version: str = Field(..., alias="Application.Version")
    session_current_user: str = Field(..., alias="Session.CurrentUser")
    session_default_store: str = Field(..., alias="Session.DefaultStore")

    def __getattr__(self, name: str) -> Any:
        """
        Allow access via alias (with dots or underscores).
        """
        # use the class’s model_fields to avoid instance deprecation
        fields = type(self).model_fields

        # direct alias match
        for attr, info in fields.items():
            if info.alias == name:
                return getattr(self, attr)

        # underscore-normalized alias
        alt = name.replace("_", ".")
        for attr, info in fields.items():
            if info.alias == alt:
                return getattr(self, attr)

        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

# src/outlook_categories/models.py

from typing import Dict, List
from pydantic import RootModel
from .models import OutlookCategory  # assuming OutlookCategory is already defined here

class OutlookCategories(RootModel[Dict[str, List[OutlookCategory]]]):
    """
    A root model for the mapping from schema‐UUID to a list of OutlookCategory objects.

    JSON form:
    {
      "<schema‐UUID>": [
        { … OutlookCategory … },
        { … }
      ]
    }
    """
    pass
