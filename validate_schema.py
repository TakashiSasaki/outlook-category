import yaml
import requests
import jsonschema

# YAML スキーマの取得元（GitHub RAW URL）
url = "https://raw.githubusercontent.com/TakashiSasaki/outlook-category/master/schemas/OutlookCategory.yaml"

# YAML をロードして Python dict に変換
doc = yaml.safe_load(requests.get(url).text)

# 'OutlookCategory' スキーマ部分だけ抽出
schema = doc.get("OutlookCategory")

if not schema:
    raise ValueError("Missing 'OutlookCategory' top-level key in schema")

# スキーマ自体をチェック（Draft 2020-12）
jsonschema.Draft202012Validator.check_schema(schema)
print("✅ OutlookCategory schema is valid JSON Schema Draft 2020-12.")
