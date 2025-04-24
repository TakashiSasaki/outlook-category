#!/usr/bin/env python3
# scripts/print_outlook_category_schema.py

"""
Generate and print the JSON Schema for OutlookCategory using Pydantic v2,
with model attribute names as keys.
"""

import json
from outlook_categories.models import OutlookCategory

def main():
    # Generate schema (uses internal field names, e.g. "account", "category_id", etc.)
    schema = OutlookCategory.model_json_schema()
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    main()
