#!/usr/bin/env python3
# scripts/print_outlook_categories_schema.py

"""
Generate and print the JSON Schema for the OutlookCategories root model
(using alias names for properties).
"""

import json
from outlook_categories.models import OutlookCategories

def main():
    # Produce JSON Schema with alias names (i.e. the UUID property)
    schema = OutlookCategories.model_json_schema(by_alias=True)
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    main()
