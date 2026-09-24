#!/usr/bin/env python3
"""Static validation for the Trivium Russian localization catalog."""

from __future__ import annotations

import ast
import json
import string
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "locales" / "ru.json"
SCAN_ROOTS = (
    ROOT / "api",
    ROOT / "bot",
    ROOT / "cogs",
    ROOT / "config",
    ROOT / "database",
    ROOT / "main.py",
)


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file, object_pairs_hook=reject_duplicate_keys)


def flatten(node, prefix=""):
    flat = {}
    if not isinstance(node, dict):
        raise TypeError("locale root must be a JSON object")

    for key, value in node.items():
        dotted = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten(value, dotted))
        elif isinstance(value, str):
            flat[dotted] = value
        else:
            raise TypeError(
                f"translation leaf must be a string: {dotted} "
                f"(got {type(value).__name__})"
            )
    return flat


def python_files():
    for root in SCAN_ROOTS:
        if root.is_file():
            yield root
        elif root.is_dir():
            yield from sorted(root.rglob("*.py"))


def literal_translation_calls(path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "t":
            continue
        if not node.args:
            continue

        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            yield first.value, node.lineno


def validate_format_strings(flat):
    formatter = string.Formatter()
    errors = []
    for key, value in flat.items():
        try:
            list(formatter.parse(value))
        except ValueError as exc:
            errors.append(f"{key}: invalid format string: {exc}")
    return errors


def main():
    try:
        catalog = load_catalog()
        flat = flatten(catalog)
    except Exception as exc:
        print(f"ERROR: {CATALOG_PATH}: {exc}", file=sys.stderr)
        return 1

    errors = validate_format_strings(flat)
    literal_calls = 0

    for path in python_files():
        try:
            calls = list(literal_translation_calls(path))
        except SyntaxError as exc:
            errors.append(f"{path.relative_to(ROOT)}:{exc.lineno}: {exc.msg}")
            continue

        for key, lineno in calls:
            literal_calls += 1
            if key not in flat:
                errors.append(
                    f"{path.relative_to(ROOT)}:{lineno}: "
                    f"missing translation key {key!r}"
                )

    if errors:
        print("Localization validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"i18n=OK catalog_strings={len(flat)} "
        f"literal_translation_calls={literal_calls}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
