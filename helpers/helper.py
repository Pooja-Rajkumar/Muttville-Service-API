from datetime import datetime
from typing import Any


def clean_string(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()

    return text or None

def parse_timestamp(value: Any) -> datetime | None: # type: ignore
    text = clean_string(value)

    if not text:
        return None

    formats = (
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
    )

    for date_format in formats:
        try:
            return datetime.strptime(text, date_format)
        except ValueError:
            continue

    return None