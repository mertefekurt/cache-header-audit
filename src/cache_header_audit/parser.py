from __future__ import annotations


def normalize_headers(headers: dict[str, str]) -> dict[str, str]:
    return {key.lower(): value.strip() for key, value in headers.items()}


def parse_cache_control(value: str | None) -> dict[str, str | bool]:
    """Parse a Cache-Control header into lowercase directives and values."""
    if not value:
        return {}

    directives: dict[str, str | bool] = {}
    for raw_part in value.split(","):
        part = raw_part.strip()
        if not part:
            continue

        if "=" not in part:
            directives[part.lower()] = True
            continue

        key, raw_value = part.split("=", 1)
        directives[key.strip().lower()] = raw_value.strip().strip('"')

    return directives


def parse_int(value: str | bool | None) -> int | None:
    if value is None or isinstance(value, bool):
        return None

    try:
        return int(value)
    except ValueError:
        return None
