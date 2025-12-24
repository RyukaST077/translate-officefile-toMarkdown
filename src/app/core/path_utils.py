"""Path utility helpers for scanning and output planning."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = frozenset({".docx", ".xls", ".xlsx"})


def is_supported_extension(path: Path, extensions: Iterable[str] | None = None) -> bool:
    """Return True if the path's extension is in the supported set (case-insensitive)."""
    if extensions is None:
        normalized = SUPPORTED_EXTENSIONS
    else:
        normalized = {ext.lower() for ext in extensions}
    return path.suffix.lower() in normalized


def is_temp_office_file(path: Path) -> bool:
    """Return True for Office temporary files (e.g. '~$foo.docx')."""
    return path.name.startswith("~$")


def is_excluded_output_dir_name(name: str) -> bool:
    """Return True if a directory name should be excluded from scanning."""
    return "_md" in name.lower()


def relative_to_root(path: Path, root: Path) -> Path:
    """Return path relative to root, raising ValueError if outside."""
    return path.resolve().relative_to(root.resolve())
