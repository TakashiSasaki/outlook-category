#!/usr/bin/env python
# src/outlook_categories/get_outlook_categories.py

"""
Module for retrieving Outlook categories via the COM API and emitting JSON to stdout.
Provides a function to return categories as a dict keyed by schema UUID, mapping to a list of dictionaries.
"""

import json
import sys
import win32com.client
from typing import Dict, List, Any

# This must match the x-id / urn:uuid of OutlookCategoryArray.json
SCHEMA_UUID = "8f87b8d1-cc90-4e92-b295-b2222efcbf28"


def resolve_class_name(value: int) -> str:
    """
    Map OlObjectClass numeric values to human-readable names.
    """
    class_map = {
        152: 'olCategory',
        153: 'olCategories',
    }
    return class_map.get(value, f'Unknown({value})')


def get_outlook_categories() -> Dict[str, List[Dict[str, Any]]]:
    """
    Retrieve Outlook categories across all MAPI stores.

    Returns:
        A dict whose single key is the schema UUID, and whose value is
        a list of category dicts.
    """
    outlook = win32com.client.Dispatch('Outlook.Application')
    namespace = outlook.GetNamespace('MAPI')
    categories_list: List[Dict[str, Any]] = []

    for store in namespace.Stores:
        store_name = store.DisplayName
        session = store.GetRootFolder().Session
        for category in session.Categories:
            info: Dict[str, Any] = {
                'Account': store_name,
                'CategoryID': category.CategoryID,
                'Color': category.Color,
                'Name': category.Name,
                'ClassName': resolve_class_name(category.Class),
                'Application.Name': outlook.Name,
                'Application.Version': outlook.Version,
                'Session.CurrentUser': session.CurrentUser.Name,
                'Session.DefaultStore': session.DefaultStore.DisplayName,
            }
            categories_list.append(info)

    return {SCHEMA_UUID: categories_list}


def main():
    """
    Entry point: retrieve categories and write JSON object to stdout.
    """
    result = get_outlook_categories()
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
