"""Basic smoke tests to ensure the package can be imported."""

from __future__ import annotations

from pathlib import Path
import sys


def test_app_package_imports() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    sys.path.insert(0, str(src_path))
    try:
        import app  # noqa: F401
    finally:
        sys.path.remove(str(src_path))
