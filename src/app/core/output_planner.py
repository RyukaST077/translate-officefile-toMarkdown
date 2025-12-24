"""Output directory and file planning utilities."""

from __future__ import annotations

import itertools
from pathlib import Path

from .path_utils import relative_to_root


def plan_output_dir(input_dir: Path) -> Path:
    """Return a non-existing output directory path next to the input directory.

    Naming rule: <input>_md, <input>_md_2, <input>_md_3, ...
    """
    base_name = f"{input_dir.name}_md"
    parent = input_dir.parent
    for index in itertools.count(1):
        name = base_name if index == 1 else f"{base_name}_{index}"
        candidate = parent / name
        if not candidate.exists():
            return candidate
    raise RuntimeError("Failed to plan output directory.")


def plan_output_file(
    input_file: Path,
    input_root: Path,
    output_root: Path,
) -> Path:
    """Return a non-conflicting output file path under output_root.

    Relative path under input_root is preserved, and the extension is .md.
    Naming rule for collisions: a.md, a_2.md, a_3.md, ...
    """
    relative_path = relative_to_root(input_file, input_root)
    candidate = (output_root / relative_path).with_suffix(".md")
    return _resolve_file_collision(candidate)


def _resolve_file_collision(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    for index in itertools.count(2):
        candidate = path.with_name(f"{stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("Failed to plan output file path.")
