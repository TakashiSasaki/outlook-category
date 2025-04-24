# Outlook Category Export & Validation

A Python package and CLI tool to export Microsoft Outlook categories via the COM API and validate them against a JSON Schema.

## Features

- **Export**: Retrieve all categories from every MAPI store in Outlook and emit JSON to stdout  
- **Module API**: `get_outlook_categories()` returns a `List[Dict[str, Any]]` you can import in your own scripts  
- **Validation**: Verify exported JSON against `OutlookCategoryArray.json` schema with Pydantic models or JSON Schema  
- **Tooling**: Built-in `doit` tasks for linting, schema-check, export & validation, and unit tests

---

## Installation

You need Windows with Outlook installed, and Python ≥ 3.9.

1. Clone the repo and enter the directory:

   ```bash
   git clone https://github.com/TakashiSasaki/outlook-category.git
   cd outlook-category
   ```

2. Install dependencies (including dev tools):

   ```bash
   python -m poetry install --with dev
   ```

---

## Usage

### CLI Export

```powershell
poetry run python -m outlook_categories.get_outlook_categories \
  > outlook_categories.json
```

Or, if you have a console script entry (after `poetry install`):

```bash
export-outlook-categories > outlook_categories.json
```

### Programmatic API

```python
from outlook_categories.get_outlook_categories import get_outlook_categories

categories = get_outlook_categories()
for cat in categories:
    print(cat["Name"], cat["Color"])
```

---

## Validation

### JSON Schema

```bash
poetry run python validate_data.py
```

This will:

1. Run the PowerShell exporter  
2. Load `outlook_categories.json`  
3. Validate it against `schemas/OutlookCategoryArray.json`

### Pydantic

```python
from outlook_categories.models import OutlookCategory
from outlook_categories.get_outlook_categories import get_outlook_categories

raw = get_outlook_categories()
typed = [OutlookCategory.parse_obj(item) for item in raw]
```

---

## Development

We use [`doit`](https://pydoit.org/) to orchestrate checks:

| Task               | Command                     | What it does                             |
|--------------------|-----------------------------|------------------------------------------|
| **health** (default) | `poetry run doit`          | lint → schema → export & validate        |
| **lint**           | `poetry run doit lint`      | `ruff` & `black --check`                 |
| **schema**         | `poetry run doit validate_schema` | Validate JSON Schema syntax (Draft 2020-12) |
| **export**         | `poetry run doit export`    | Run export+validation via `validate_data.py` |
| **test**           | `poetry run pytest`         | Unit tests (including Pydantic models)   |

You can also run individual steps, e.g.:

```bash
poetry run doit lint
poetry run doit validate_schema
poetry run doit export
poetry run pytest
```

---

## Project Layout

```
├─ src/
│   └─ outlook_categories/
│       ├─ __init__.py
│       ├─ get_outlook_categories.py
│       └─ models.py
├─ schemas/
│   ├─ OutlookCategory.json
│   └─ OutlookCategoryArray.json
├─ tests/
│   └─ test_get_outlook_categories.py
├─ dodo.py
├─ validate_data.py
├─ pyproject.toml
└─ .vscode/
    └─ settings.json
```

---

## Contributing

1. Fork & clone  
2. Create a feature branch  
3. Run `poetry run doit` to ensure everything passes  
4. Submit a pull request  

---

## License

MIT © Takashi Sasaki  
