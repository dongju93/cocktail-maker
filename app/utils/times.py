from datetime import UTC, datetime


def unix_to_datetime(unix_time: float) -> datetime:
    return datetime.fromtimestamp(unix_time, tz=UTC)


def datetime_now() -> datetime:
    return datetime.now(tz=UTC)
