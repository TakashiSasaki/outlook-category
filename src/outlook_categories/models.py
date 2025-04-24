from pydantic import BaseModel, Field
from typing import Any, Dict


class OutlookCategory(BaseModel):
    Account: str
    CategoryID: str
    Color: int
    Name: str
    ClassName: str

    Application_Name: str = Field(..., alias="Application.Name")
    Application_Version: str = Field(..., alias="Application.Version")
    Session_CurrentUser: str = Field(..., alias="Session.CurrentUser")
    Session_DefaultStore: str = Field(..., alias="Session.DefaultStore")

    class Config:
        # allow input using the dotted keys
        allow_population_by_field_name = True  
        # when you call .dict(by_alias=True), it will emit dotted keys again
        allow_population_by_alias = True


# Example usage:
raw: Dict[str, Any] = {
    "Account": "foo@example.com",
    "CategoryID": "{...}",
    "Color": 3,
    "Name": "MyCat",
    "ClassName": "olCategory",
    "Application.Name": "Outlook",
    "Application.Version": "16.0.1234",
    "Session.CurrentUser": "You",
    "Session.DefaultStore": "you@example.com",
}

# Validate & parse:
obj = OutlookCategory.parse_obj(raw)

# Access via Python attributes:
print(obj.Application_Name)  # Outlook

# Round-trip back to dotted-key dict:
validated_dict = obj.dict(by_alias=True)
assert "Application.Name" in validated_dict
