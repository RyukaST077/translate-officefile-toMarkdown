"""Progress event models for UI updates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProgressEvent:
    """Represents progress for a single conversion step."""

    index: int
    total: int
    current_file: Path

    @property
    def percent(self) -> float:
        if self.total <= 0:
            return 0.0
        return (self.index / self.total) * 100.0
