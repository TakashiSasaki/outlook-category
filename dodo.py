from pathlib import Path
import yaml
import jsonschema


def task_validate_schema():
    """
    Validate the OutlookCategoryArray.yaml schema using JSON Schema Draft 2020-12.
    """
    schema_file = Path("schemas/OutlookCategoryArray.yaml")

    def validate():
        with schema_file.open("r", encoding="utf-8") as f:
            schema = yaml.safe_load(f)

        jsonschema.Draft202012Validator.check_schema(schema)
        print("✅ OutlookCategoryArray schema is valid JSON Schema Draft 2020-12.")

    return {
        "actions": [validate],
        "file_dep": [str(schema_file)],
        "verbosity": 2,  # 明示的に出力
        "doc": "Validate that the OutlookCategoryArray.yaml is a valid array schema"
    }
