"""Schema comparison with normalized semantic types."""

from typing import Any


def _normalize_type(value: str) -> str:
    value = str(value).strip().lower()

    aliases = {
        "str": "object",
        "string": "object",
        "string[python]": "object",
        "string[pyarrow]": "object",
    }

    return aliases.get(value, value)


def compare(
    expected: dict[str, str],
    actual: dict[str, str],
) -> dict[str, Any]:
    expected = {
        str(key): _normalize_type(value)
        for key, value in expected.items()
    }

    actual = {
        str(key): _normalize_type(value)
        for key, value in actual.items()
    }

    added = sorted(set(actual) - set(expected))
    removed = sorted(set(expected) - set(actual))

    changed = sorted(
        key
        for key in set(expected) & set(actual)
        if expected[key] != actual[key]
    )

    return {
        "drift": bool(added or removed or changed),
        "added": added,
        "removed": removed,
        "type_changed": changed,
        "expected": expected,
        "actual": actual,
    }
