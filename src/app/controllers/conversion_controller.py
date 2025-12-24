"""Controller for running conversions in a background thread."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import threading
from typing import Callable

from app.config import LOG_FILE_NAME
from app.core.document_converter import convert_document
from app.core.file_scanner import scan_input_files
from app.core.logger import ConversionLogger
from app.core.output_planner import plan_output_dir, plan_output_file
from app.models.progress_event import ProgressEvent


@dataclass(frozen=True)
class ConversionSummary:
    """Summary of a conversion run."""

    output_dir: Path
    log_path: Path
    total: int
    success_count: int
    failure_count: int
    warning_count: int


OnStart = Callable[[Path, int], None]
OnProgress = Callable[[ProgressEvent], None]
OnComplete = Callable[[ConversionSummary], None]
OnError = Callable[[Exception], None]
Dispatcher = Callable[[Callable[[], None]], None]


class ConversionController:
    """Run conversion workload and report progress back to the UI."""

    def __init__(
        self,
        dispatch: Dispatcher,
        on_start: OnStart,
        on_progress: OnProgress,
        on_complete: OnComplete,
        on_error: OnError,
    ) -> None:
        self._dispatch = dispatch
        self._on_start = on_start
        self._on_progress = on_progress
        self._on_complete = on_complete
        self._on_error = on_error
        self._lock = threading.Lock()
        self._running = False

    def start(self, input_dir: Path) -> bool:
        """Start conversion if not already running."""
        with self._lock:
            if self._running:
                return False
            self._running = True

        thread = threading.Thread(
            target=self._run,
            args=(input_dir,),
            name="conversion-worker",
            daemon=True,
        )
        thread.start()
        return True

    def _run(self, input_dir: Path) -> None:
        try:
            if not input_dir.exists():
                raise FileNotFoundError(input_dir)
            if not input_dir.is_dir():
                raise NotADirectoryError(input_dir)

            output_dir = plan_output_dir(input_dir)
            output_dir.mkdir(parents=True, exist_ok=False)
            log_path = output_dir / LOG_FILE_NAME
            logger = ConversionLogger(log_path)
            logger.info(f"Input folder: {input_dir}")

            files = scan_input_files(input_dir)
            total = len(files)
            self._dispatch(
                lambda output_dir=output_dir, total=total: self._on_start(
                    output_dir,
                    total,
                )
            )

            if total == 0:
                logger.warning("対象ファイルが見つかりませんでした。")

            success_count = 0
            failure_count = 0
            warning_count = 0

            for index, path in enumerate(files, start=1):
                event = ProgressEvent(index=index, total=total, current_file=path)
                self._dispatch(lambda event=event: self._on_progress(event))

                try:
                    result = convert_document(path)
                    output_file = plan_output_file(path, input_dir, output_dir)
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    output_file.write_text(result.markdown, encoding="utf-8")
                    success_count += 1
                    logger.info(f"SUCCESS: {path} -> {output_file}")

                    for warning in result.warnings:
                        warning_count += 1
                        logger.warning(f"{path}: {warning}")
                except Exception as exc:  # pragma: no cover - runtime safety
                    failure_count += 1
                    logger.error(f"FAILED: {path}: {exc}")

            summary = ConversionSummary(
                output_dir=output_dir,
                log_path=log_path,
                total=total,
                success_count=success_count,
                failure_count=failure_count,
                warning_count=warning_count,
            )
            logger.info(
                "Completed. "
                f"total={total} success={success_count} "
                f"failure={failure_count} warnings={warning_count}"
            )
            self._dispatch(lambda summary=summary: self._on_complete(summary))
        except Exception as exc:  # pragma: no cover - runtime safety
            self._dispatch(lambda exc=exc: self._on_error(exc))
        finally:
            with self._lock:
                self._running = False
