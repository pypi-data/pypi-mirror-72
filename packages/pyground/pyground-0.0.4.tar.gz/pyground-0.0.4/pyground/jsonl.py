from typing import Any, Iterable
import json


def dump(items: Iterable[Any], fp, *, separators=(",", ":"), **kwargs):
    """
    Much like json.dump followed by writing a newline, but with two changes:
    * `indent` is forced to None
    * `separators` defaults to the more compact version, but can be overridden
    """
    for item in items:
        json.dump(item, fp, indent=None, separators=separators, **kwargs)
        fp.write("\n")


def dumps(items: Iterable[Any], *, separators=(",", ":"), **kwargs) -> str:
    return "".join(
        chunk
        for item in items
        for chunk in (
            json.dumps(item, indent=None, separators=separators, **kwargs),
            "\n",
        )
    )
