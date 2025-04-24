from pathlib import Path
import yaml
import jsonschema


def task_validate_schema():
    """
    Validate the OutlookCategory.yaml schema using JSON Schema Draft 2020-12.
    """
    schema_file = Path("schemas/OutlookCategory.yaml")

    def validate():
        with schema_file.open("r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)

        if "OutlookCategory" not in doc:
            raise ValueError("Missing top-level key: OutlookCategory")

        schema = doc["OutlookCategory"]
        jsonschema.Draft202012Validator.check_schema(schema)
        print("✅ OutlookCategory schema is valid JSON Schema Draft 2020-12.")

    return {
        "actions": [validate],
        "file_dep": [str(schema_file)],
        "verbosity": 2,
        "doc": "Validate that the OutlookCategory.yaml file is a valid JSON Schema"
    }
