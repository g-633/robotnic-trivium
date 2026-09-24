import json
from functools import lru_cache

from config.paths import ROOT


LOCALE_PATH = ROOT / "locales" / "ru.json"


@lru_cache(maxsize=1)
def _load_catalog() -> dict:
    with LOCALE_PATH.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    if not isinstance(catalog, dict):
        raise TypeError(f"Locale catalog must be a JSON object: {LOCALE_PATH}")

    return catalog


def t(key: str, **values) -> str:
    """Return a Russian UI string by dotted key and format its placeholders."""
    value = _load_catalog()

    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"Missing translation key: {key}")
        value = value[part]

    if not isinstance(value, str):
        raise TypeError(f"Translation key is not a string: {key}")

    return value.format(**values)
