#!/usr/bin/env python3
# scripts/print_outlook_category_schema_alias.py

"""
Generate and print the JSON Schema for OutlookCategory using Pydantic v2,
with alias names used as JSON property keys.
"""

import json
from outlook_categories.models import OutlookCategory

def main():
    # Generate schema using alias names (e.g. "Account", "CategoryID", ...)
    schema = OutlookCategory.model_json_schema(by_alias=True)
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    main()
