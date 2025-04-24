# src/outlook_categories/models.py

from typing import Any, Dict, Literal
from pydantic import BaseModel, Field, ConfigDict
class OutlookCategory(BaseModel):
    model_config = ConfigDict(
      populate_by_name=True,
      extra="ignore",
      title="Outlook Category Export Schema (Unified)",
      json_schema_extra={
        "$id": "https://raw.githubusercontent.com/TakashiSasaki/outlook-category/master/schemas/OutlookCategory.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "x-id":   "urn:uuid:fd0cf529-cbf4-4fc6-a92f-86f357c6e51e",
        "x-version": "1.0.0",
        "x-created": "2025-04-24",
        "x-createdBy": {
          "name": "Takashi Sasaki",
          "homepage": "https://x.com/TakashiSasaki"
        },
        "x-license": {
          "name": "MIT",
          "url": "https://opensource.org/licenses/MIT"
        },
        "x-repository": "https://github.com/TakashiSasaki/outlook-category"
      }
    )
    # core, required fields:
    account: str = Field(..., alias="Account",
      description="Display name or email address of the Outlook store …")
    category_id: str = Field(..., alias="CategoryID", pattern=r"^\{[0-9A-Fa-f\-]{36}\}$",
      description="Globally unique identifier for the category …")
    color: int = Field(..., alias="Color", ge=0, le=25,
      description="Integer corresponding to the OlCategoryColor enumeration …")
    name: str = Field(..., alias="Name",
      description="Human-readable name of the category …")
    class_name: Literal["olCategory"] = Field(..., alias="ClassName",
      description="Resolved value of the category class (typically 'olCategory'). …")

    # now optional detailed fields:
    application_name:  str | None = Field(None, alias="Application.Name",
      description="Name of the application providing the category object …")
    application_version: str | None = Field(None, alias="Application.Version",
      description="Version string of the Outlook application …")
    session_current_user:  str | None = Field(None, alias="Session.CurrentUser",
      description="Display name of the user associated with the current Outlook session …")
    session_default_store: str | None = Field(None, alias="Session.DefaultStore",
      description="Display name or email address of the default store in the session …")

    # (keep your __getattr__ hack if you still need it)

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
