"""
Regex-based timestamp recognizer / parser / extractor.
"""
from typing import List, Union
import datetime
import re


def named_group(r: str, name: str) -> str:
    return fr"(?P<{name}>{r})"


######
# date
year = r"20[012][0-9]"  # 2000–2029
year_named = named_group(year, "year")
month = r"0[1-9]|1[0-2]"  # 01–12
month_named = named_group(month, "month")
day = r"0[1-9]|[12][0-9]|3[01]"  # 01–31
day_named = named_group(day, "day")
# date separator can be dash, space, slash, or nothing
dateSep = r"[- /]?"
# month and day are both optional, but if month is omitted, day is prohibited
# n.b.: (?P=my) is a backreference to a preceding (?P<my>...)
date = fr"{year_named}((?P<dateSep>{dateSep}){month_named}((?P=dateSep){day_named})?)?"

######
# time
hour24 = r"[0-1][0-9]|2[0-4]"  # 00–24
hour24_named = named_group(hour24, "hour24")
hour12 = r"0[0-9]|1[0-2]"  # 00–12
hour12_named = named_group(hour12, "hour12")
sixty = r"[0-5][0-9]"  # 00–59
# time separator can be dash (U+002D "HYPHEN-MINUS"), period (U+0023 "FULL STOP"), colon (U+003A), or nothing
timeSep = r"[-.:]?"
# minute and second are both optional, but if minute is omitted, second is prohibited
time12 = fr"{hour12_named}((?P<timeSep12>{timeSep}){named_group(sixty, 'minute12')}((?P=timeSep12){named_group(sixty, 'second12')})?)? ?(?P<meridian>AM|PM|am|pm)"
time24 = fr"{hour24_named}((?P<timeSep24>{timeSep}){named_group(sixty, 'minute24')}((?P=timeSep24){named_group(sixty, 'second24')})?)?"
# n.b. hour12 + meridian needs to be greedier than hour24 search
time = fr"({time12}|{time24})"

###############
# date_and_time
# datetime separator can be "T", space, nothing, or " at "
datetimeSep = "(T| || at )"
# time is optional
date_and_time = fr"{date}({datetimeSep}{time})?"


def _match_datetime(m: re.Match) -> Union[datetime.datetime, datetime.date]:
    groupdict = m.groupdict()
    # n.b. we do not care about the separators when parsing
    date_parts = int(groupdict["year"]), int(groupdict["month"]), int(groupdict["day"])
    if groupdict["meridian"]:
        # 12-hour datetime
        meridian = groupdict["meridian"]
        hour = int(groupdict["hour12"])
        # usually "pm" means "add 12 hours to get 24-hour time" except for "12... pm"
        if meridian.lower() == "pm" and hour != 12:
            hour += 12
        minute = int(groupdict["minute12"] or "0")
        second = int(groupdict["second12"] or "0")
        return datetime.datetime(*date_parts, hour, minute, second)
    if groupdict["hour24"]:
        # 24-hour datetime
        hour = int(groupdict["hour24"])
        minute = int(groupdict["minute24"] or "0")
        second = int(groupdict["second24"] or "0")
        return datetime.datetime(*date_parts, hour, minute, second)
    # date only
    return datetime.date(*date_parts)


def _extract_timestamp(string: str) -> tuple:
    # prefix and suffix are padding around the timestamp part of the string
    m = re.search(fr"(?P<prefix>^| |-|_){date_and_time}(?P<suffix>[- _]||$)", string)
    if not m:
        raise ValueError(f"No timestamp found in {string!r}")
    start, end = m.span()
    before = string[:start]
    after = string[end:]
    prefix = m.groupdict()["prefix"]
    suffix = m.groupdict()["suffix"]
    timestamp = _match_datetime(m)
    return before, prefix, timestamp, suffix, after


def _format_timestamp(timestamp: Union[datetime.datetime, datetime.date]) -> str:
    """
    Convert to ISO-8601 format without intra-date or intra-time separators,
    and using Z alias for UTC (instead of default "+00:00").
    """
    # always return year/month/day
    fmt = "%Y%m%d"
    # n.b. datetime is a subclass of date (but not vice-versa)
    if isinstance(timestamp, datetime.datetime):
        fmt += "T%H%M%S"
        offset: datetime.timedelta = timestamp.utcoffset()
        # if dt is naive, offset will be None
        if offset is not None:
            # if offset is 0 (indicating UTC), bool(offset) => False
            if not offset:
                fmt += "Z"
            else:
                fmt += "%z"
    return timestamp.strftime(fmt)


def hoist_timestamp(string: str) -> str:
    """
    Move timestamp to beginning of string, if possible; otherwise return string unchanged.
    """
    try:
        before, prefix, timestamp, suffix, after = _extract_timestamp(string)
        return f"{_format_timestamp(timestamp)}{prefix}{before}{suffix}{after}"
    except ValueError:
        return string


if __name__ == "__main__":
    # Use like:
    #   python -m pyground.timestamps *.png -n
    from pathlib import Path
    import logging

    import click

    @click.command()
    @click.argument("paths", type=click.Path(exists=True), nargs=-1)
    @click.option("-v", "--verbose", count=True, help="Increase logging verbosity.")
    @click.option(
        "-n",
        "--dry-run",
        is_flag=True,
        help="Don't do anything, just log changes that would be made.",
    )
    def main(paths: List[str] = (), verbose: int = 0, dry_run: bool = False):
        """
        Hoist timestamp for each given path, ignoring files with no recognizable timestamp.
        """
        logging_level = logging.INFO - (verbose * 10)
        logging_format = "%(asctime)14s %(levelname)-7s %(name)s - %(message)s"
        logging.basicConfig(format=logging_format, level=logging_level)
        logging.debug(
            "Set logging level to %s [%d]",
            logging.getLevelName(logging_level),
            logging_level,
        )

        logger = logging.getLogger("pyground-timestamps")

        for path in map(Path, paths):
            old_name = path.name
            new_name = hoist_timestamp(old_name)
            if new_name == old_name:
                logger.debug("'%s' unchanged", path)
                continue
            new_path = path.with_name(new_name)
            if new_path.exists():
                logger.error("'%s' already exists", new_path)
                continue
            if dry_run:
                logger.info("[no-op] Would move '%s' -> '%s'", path, new_path)
                continue
            logger.info("Moving '%s' -> '%s'", path, new_path)
            path.rename(new_path)

    main()
