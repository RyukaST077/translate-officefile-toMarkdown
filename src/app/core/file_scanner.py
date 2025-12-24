"""File scanning utilities for input folders."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .path_utils import (
    SUPPORTED_EXTENSIONS,
    is_excluded_output_dir_name,
    is_supported_extension,
    is_temp_office_file,
)


@dataclass(frozen=True)
class FileScanError(RuntimeError):
    """Raised when an input directory cannot be fully scanned."""

    path: Path
    original: OSError

    def __str__(self) -> str:
        return f"Failed to scan {self.path}: {self.original}"


def scan_input_files(input_root: Path) -> list[Path]:
    """Recursively scan for supported document files under input_root.

    Exclusions:
    - Temporary Office files that start with '~$'.
    - Directories whose names contain '_md' (case-insensitive).

    Raises:
    - FileNotFoundError or NotADirectoryError when input_root is invalid.
    - FileScanError when access to a path is denied or another OS error occurs.
    """
    if not input_root.exists():
        raise FileNotFoundError(input_root)
    if not input_root.is_dir():
        raise NotADirectoryError(input_root)

    collected: list[Path] = []

    def onerror(error: OSError) -> None:
        raise FileScanError(Path(error.filename) if error.filename else input_root, error)

    for dirpath, dirnames, filenames in os.walk(input_root, onerror=onerror):
        dirnames[:] = [
            name for name in dirnames if not is_excluded_output_dir_name(name)
        ]

        for filename in filenames:
            path = Path(dirpath) / filename
            if is_temp_office_file(path):
                continue
            if is_supported_extension(path, SUPPORTED_EXTENSIONS):
                collected.append(path)

    return sorted(collected)
