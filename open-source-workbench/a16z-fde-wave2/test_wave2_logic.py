"""Focused, dependency-free regression checks for the Wave 2 proposal logic.

These exercise extracted logic only; they are not a substitute for upstream tests.
"""
import json
import re
import shlex
from pathlib import Path

class InvalidError(Exception):
    pass

def extract_copy_command_patterns(dockerfile_lines):
    copy_source_patterns = set()
    current_command = ""
    copy_pattern = re.compile(r"^\s*COPY\s+(.+)$", re.IGNORECASE)
    for line in dockerfile_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if current_command:
            current_command += " " + line.rstrip("\\").strip()
        else:
            current_command = line.rstrip("\\").strip()
        if not line.endswith("\\"):
            match = copy_pattern.match(current_command)
            if match:
                args = match.group(1)
                flags_match = re.match(r"^((?:--[^\s]+\s+)*)(.*)$", args)
                flags, remainder = flags_match.groups() if flags_match else ("", args)
                try:
                    json_parts = json.loads(remainder) if remainder.startswith("[") else None
                except json.JSONDecodeError:
                    json_parts = None
                if isinstance(json_parts, list) and len(json_parts) >= 2 and all(isinstance(part, str) for part in json_parts):
                    parts = shlex.split(flags) + json_parts
                else:
                    parts = shlex.split(args)
                if any(p.startswith("--from=") for p in parts):
                    current_command = ""
                    continue
                known_flag_prefixes = ("--chmod=", "--chown=", "--link=")
                parts = [p for p in parts if p != "--link" and not any(p.startswith(prefix) for prefix in known_flag_prefixes)]
                if len(parts) >= 2:
                    for source in parts[:-1]:
                        if re.compile(r"^\s*--|\$\s*").match(source):
                            raise InvalidError(source)
                        if source.rstrip("/") == ".":
                            copy_source_patterns.add("./**")
                        else:
                            copy_source_patterns.add(source)
            current_command = ""
    return copy_source_patterns

cases = [
    ('COPY ["files/dir1", "/dest/"]', {"files/dir1"}),
    ('COPY ["files/my dir/a.txt", "/dest/"]', {"files/my dir/a.txt"}),
    ('COPY --chown=1000:1000 ["files/a.txt", "files/b.txt", "/dest/"]', {"files/a.txt", "files/b.txt"}),
    ("COPY ./ /dest/", {"./**"}),
    ("COPY . /dest/", {"./**"}),
    ("COPY --from=stage /app /dest", set()),
]
for command, expected in cases:
    got = extract_copy_command_patterns([command])
    assert got == expected, (command, got, expected)

def read_ignorefile(text):
    excludes = []
    for line in text.splitlines():
        pattern = line.rstrip("\n\r")
        if pattern.startswith("#"):
            continue
        pattern = pattern.strip()
        if not pattern:
            continue
        invert = pattern[0] == "!"
        if invert:
            pattern = pattern[1:].strip()
        if pattern:
            pattern = Path(pattern).as_posix()
            if len(pattern) > 1 and pattern.startswith("/"):
                pattern = pattern[1:]
        if invert:
            pattern = "!" + pattern
        excludes.append(pattern)
    return excludes

assert read_ignorefile("*.txt\n!/keep.txt\n") == ["*.txt", "!keep.txt"]

import os
import tempfile
with tempfile.TemporaryDirectory() as tmp:
    original_cwd = Path.cwd()
    root = Path(tmp).resolve()
    project = root / "project"
    project.mkdir()
    specific = project / "Dockerfile.dockerignore"
    specific.write_text("**/*.py")
    try:
        os.chdir(root)
        dockerfile_relative = Path("project/Dockerfile")
        context = Path.cwd().absolute()
        dockerfile = dockerfile_relative.absolute()
        candidate = dockerfile.parent / f"{dockerfile.name}.dockerignore"
        assert candidate.is_relative_to(context)
        assert candidate == specific
    finally:
        os.chdir(original_cwd)

print("Wave 2 isolated regression checks passed: 8 checks")
