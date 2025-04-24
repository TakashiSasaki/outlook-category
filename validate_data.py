import subprocess
import json
import jsonschema
from pathlib import Path

# JSONベースのスキーマファイルとデータファイル
SCHEMA_PATH = Path("schemas/OutlookCategoryArray.json")
DATA_PATH = Path("outlook_categories.json")
EXPORT_SCRIPT = Path("Export-OutlookCategoriesToJson.ps1")


def run_export_script():
    result = subprocess.run(
        [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(EXPORT_SCRIPT),
            "-OutputPath",
            str(DATA_PATH),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("PowerShell script failed")
    print("📁 Export completed:", DATA_PATH)


def validate_json():
    # スキーマをJSONとして読み込む
    with SCHEMA_PATH.open(encoding="utf-8") as f:
        schema = json.load(f)
    # データをBOM付きUTF-8対応で読み込む
    with DATA_PATH.open(encoding="utf-8-sig") as f:
        data = json.load(f)
    # バリデーション実行
    jsonschema.validate(
        instance=data, schema=schema, cls=jsonschema.Draft202012Validator
    )
    print("✅ JSON data is valid according to OutlookCategoryArray schema.")


def main():
    run_export_script()
    validate_json()


if __name__ == "__main__":
    main()
