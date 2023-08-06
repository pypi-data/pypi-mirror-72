from pathlib import Path

from pyground.filesystem import path_types, iterdfs


def test_path_types():
    file_path = Path(__file__)
    assert {"file"} <= set(path_types(file_path))

    dir_path = file_path.parent
    assert {"dir"} <= set(path_types(dir_path))

    root_path = Path("/")
    assert {"dir", "mount"} <= set(path_types(root_path))


def test_iterdfs():
    project_dir = Path(__file__).parent.parent
    project_paths = set(iterdfs(project_dir, sort=True))
    assert project_paths >= {
        project_dir / "setup.py",
        project_dir / "pyground" / "__init__.py",
        project_dir / "pyground" / "filesystem.py",
    }
