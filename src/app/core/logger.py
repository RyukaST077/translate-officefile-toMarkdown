"""Simple file logger for conversion results."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class ConversionLogger:
    """Append-only logger writing to a conversion log file."""

    log_path: Path

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARN", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def _write(self, level: str, message: str) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp}] {level}: {message}\n")
