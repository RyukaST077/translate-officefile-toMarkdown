"""Shim package to allow running `python -m app.main` from the repo root."""

from __future__ import annotations

from pathlib import Path

_src_app = Path(__file__).resolve().parent.parent / "src" / "app"
if _src_app.is_dir():
    __path__.append(str(_src_app))
