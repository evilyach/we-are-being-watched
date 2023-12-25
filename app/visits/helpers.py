from datetime import UTC, datetime, tzinfo


def timestamp_to_datetime(timestamp: int | None) -> datetime | None:
    if not timestamp:
        return None
    return datetime.fromtimestamp(timestamp)
