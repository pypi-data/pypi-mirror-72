from pathlib import Path
from typing import Iterator
import os

from .json import marshall
from .time import parse_timestamp  # also for marshall dispatch


PATH_PREDICATES = [
    ("absolute", Path.is_absolute),
    ("block_device", Path.is_block_device),
    ("char_device", Path.is_char_device),
    ("dir", Path.is_dir),
    ("fifo", Path.is_fifo),
    ("file", Path.is_file),
    ("mount", Path.is_mount),
    ("reserved", Path.is_reserved),
    ("socket", Path.is_socket),
    ("symlink", Path.is_symlink),
]


def path_types(path: Path) -> Iterator[str]:
    for name, predicate in PATH_PREDICATES:
        if predicate(path):
            yield name


def iterdfs(top: Path, sort: bool = False) -> Iterator[Path]:
    """
    Recursively walk filesystem, iterating into directories pre-order, depth-first.
    """
    yield top
    if top.is_dir():
        children = top.iterdir()
        if sort:
            children = sorted(children)
        for child in children:
            yield from iterdfs(child, sort=sort)


@marshall.register
def marshall_stat_result(sr: os.stat_result, **options) -> dict:
    return marshall(
        {
            "mode": f"{sr.st_mode:o}",  # TODO: truncate?
            "ino": sr.st_ino,
            "dev": sr.st_dev,
            # "nlink": sr.st_nlink,
            "uid": sr.st_uid,  # TODO: convert to name?
            "gid": sr.st_gid,  # TODO: convert to name?
            "size": sr.st_size,
            "atime": parse_timestamp(sr.st_atime),
            "mtime": parse_timestamp(sr.st_mtime),
            "ctime": parse_timestamp(sr.st_ctime),
            "btime": parse_timestamp(sr.st_birthtime),
        },
        **options,
    )


@marshall.register
def marshall_path(path: Path, *, root: Path = None, **options) -> dict:
    return marshall(
        {
            "path": str(path.relative_to(root) if root else path),
            "type": "|".join(sorted(set(path_types(path)) - {"absolute"})),
            "stat": path.stat(),
        },
        **options,
    )
