#!/usr/bin/env python
# Export_OutlookCategoriesToJson.py
"""
Python script to export all Outlook categories across all MAPI stores to a JSON file.
Uses the Outlook COM API via pywin32.

Usage:
    python Export_OutlookCategoriesToJson.py [-o OUTPUT] [-d]

Options:
    -o, --output   Path to output JSON file. Defaults to categories-YYYYMMDD.json
    -d, --detailed Include detailed Application and Session summaries.
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

import win32com.client

# Map OlObjectClass codes to names
def resolve_class_name(value: int) -> str:
    class_map = {
        152: 'olCategory',
        153: 'olCategories',
    }
    return class_map.get(value, f'Unknown({value})')


def main():
    parser = argparse.ArgumentParser(
        description='Export Outlook categories via COM API to JSON'    )
    parser.add_argument(
        '-o', '--output',
        default=f'categories-{datetime.now().strftime("%Y%m%d")}.json',
        help='Output JSON file path'
    )
    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Include detailed Application and Session info'
    )
    args = parser.parse_args()

    # Initialize Outlook COM
    outlook = win32com.client.Dispatch('Outlook.Application')
    namespace = outlook.GetNamespace('MAPI')

    all_categories = []
    # Iterate each store
    for store in namespace.Stores:
        store_name = store.DisplayName
        session = store.GetRootFolder().Session
        categories = session.Categories

        # Enumerate categories
        for category in categories:
            info = {
                'Account': store_name,
                'CategoryID': category.CategoryID,
                'Color': category.Color,
                'Name': category.Name,
                'ClassName': resolve_class_name(category.Class),
            }

            if args.detailed:
                # Detailed summaries
                info['Application'] = {
                    'Name': outlook.Name,
                    'Version': outlook.Version
                }
                info['Session'] = {
                    'CurrentUser': session.CurrentUser.Name,
                    'DefaultStore': session.DefaultStore.DisplayName
                }
            else:
                # Simplified fields
                info['Application.Name'] = outlook.Name
                info['Application.Version'] = outlook.Version
                info['Session.CurrentUser'] = session.CurrentUser.Name
                info['Session.DefaultStore'] = session.DefaultStore.DisplayName

            all_categories.append(info)

    # Write to JSON
    output_path = Path(args.output)
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(all_categories, f, ensure_ascii=False, indent=2)

    print(f'Export completed: {output_path}')


if __name__ == '__main__':
    main()
