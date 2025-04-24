import yaml
import requests
import jsonschema

# YAML スキーマの取得元（GitHub RAW URL） ← URLを書き換えるだけでもOK
url = "https://raw.githubusercontent.com/TakashiSasaki/outlook-category/master/schemas/OutlookCategoryArray.yaml"

# YAML をロードして Python dict に変換
doc = yaml.safe_load(requests.get(url).text)

# スキーマ自体をチェック（Draft 2020-12）
jsonschema.Draft202012Validator.check_schema(doc)
print("✅ OutlookCategoryArray schema is valid JSON Schema Draft 2020-12.")
