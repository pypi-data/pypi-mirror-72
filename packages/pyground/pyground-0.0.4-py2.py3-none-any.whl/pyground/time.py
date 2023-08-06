from datetime import date, datetime, timezone
from numbers import Number
import re

from .json import marshall


def parse_timestamp(timestamp: Number, tz: datetime.tzinfo = timezone.utc) -> datetime:
    """
    Convert epoch timestamp to datetime.
    """
    return datetime.fromtimestamp(timestamp, tz)


@marshall.register
def marshall_datetime(dt: datetime, *, timespec: str = "auto", **options) -> str:
    """
    Convert to ISO-8601 format, using Z alias for UTC.
    """
    return re.sub(r"\+00(?::00)?$", "Z", dt.isoformat(timespec=timespec))


@marshall.register
def marshall_date(d: date, **options) -> str:
    """
    Convert to ISO-8601 format.
    """
    return d.isoformat()
