"""Dependency-free contract tests for Modal #4130 output path selection."""
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

FILE = 1
DIRECTORY = 2

@dataclass
class Entry:
    path: str
    type: int


def volume_output_path(remote_path: str, destination: Path, entry: Entry):
    requested_path = PurePosixPath(remote_path.lstrip("/"))
    entry_path = PurePosixPath(entry.path.lstrip("/"))
    if destination.exists() and not destination.is_dir() and not (entry.type == FILE and entry_path == requested_path):
        raise ValueError("directory destination required")
    if entry_path == requested_path and entry.type == DIRECTORY:
        return destination, True
    if entry_path == requested_path and entry.type == FILE:
        return (destination / entry_path.name if destination.is_dir() else destination), False
    relative_path = entry_path.relative_to(requested_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError("unsafe path")
    return destination / Path(relative_path.as_posix()), False

with TemporaryDirectory() as tmp:
    root = Path(tmp)
    dest = root / "download"
    a, _ = volume_output_path("directory-repro", dest, Entry("directory-repro/a.txt", FILE))
    b, _ = volume_output_path("directory-repro", dest, Entry("directory-repro/b.txt", FILE))
    assert a == dest / "a.txt"
    assert b == dest / "b.txt"
    assert a != b

    nested, _ = volume_output_path("directory-repro", dest, Entry("directory-repro/sub/c.txt", FILE))
    assert nested == dest / "sub" / "c.txt"

    file_path, is_root = volume_output_path("logs/a.txt", dest / "renamed.txt", Entry("logs/a.txt", FILE))
    assert file_path == dest / "renamed.txt" and not is_root

    dest.mkdir()
    file_into_dir, _ = volume_output_path("logs/a.txt", dest, Entry("logs/a.txt", FILE))
    assert file_into_dir == dest / "a.txt"

    root_path, is_root = volume_output_path("directory-repro", dest, Entry("directory-repro", DIRECTORY))
    assert root_path == dest and is_root

    not_dir = root / "not-a-dir"
    not_dir.write_text("x")
    try:
        volume_output_path("directory-repro", not_dir, Entry("directory-repro/a.txt", FILE))
    except ValueError:
        pass
    else:
        raise AssertionError("expected directory destination validation")

    try:
        volume_output_path("directory-repro", dest, Entry("other/a.txt", FILE))
    except ValueError:
        pass
    else:
        raise AssertionError("expected relative_to to reject outside path")

print("Modal #4130 path contract checks passed: 8 checks")
