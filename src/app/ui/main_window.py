"""Main application window with conversion wiring."""

from __future__ import annotations

from pathlib import Path
from typing import Callable
import tkinter as tk
from tkinter import ttk

from app.controllers.conversion_controller import ConversionController, ConversionSummary
from app.core.output_planner import plan_output_dir
from app.models.progress_event import ProgressEvent


class MainWindow(ttk.Frame):
    """Tkinter UI layout and conversion wiring."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=12)
        self.master = master

        self.input_path = tk.StringVar(value="(not selected)")
        self.output_path = tk.StringVar(value="(auto-generated)")
        self.status_text = tk.StringVar(value="Idle")

        self.progress_bar: ttk.Progressbar
        self.input_button: ttk.Button
        self.run_button: ttk.Button

        self.controller = ConversionController(
            dispatch=self._dispatch,
            on_start=self._on_start,
            on_progress=self._on_progress,
            on_complete=self._on_complete,
            on_error=self._on_error,
        )

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid(row=0, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.columnconfigure(1, weight=1)

        input_label = ttk.Label(self, text="Input folder")
        input_entry = ttk.Entry(self, textvariable=self.input_path, state="readonly")
        self.input_button = ttk.Button(self, text="Browse", command=self._browse_input)

        output_label = ttk.Label(self, text="Output folder")
        output_entry = ttk.Entry(self, textvariable=self.output_path, state="readonly")

        self.run_button = ttk.Button(self, text="Run", command=self._run_conversion)

        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        status_label = ttk.Label(self, textvariable=self.status_text)

        pad = {"padx": 6, "pady": 6}
        input_label.grid(row=0, column=0, sticky="w", **pad)
        input_entry.grid(row=0, column=1, sticky="ew", **pad)
        self.input_button.grid(row=0, column=2, sticky="e", **pad)

        output_label.grid(row=1, column=0, sticky="w", **pad)
        output_entry.grid(row=1, column=1, columnspan=2, sticky="ew", **pad)

        self.run_button.grid(row=2, column=0, columnspan=3, sticky="ew", **pad)

        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky="ew", **pad)
        status_label.grid(row=4, column=0, columnspan=3, sticky="w", **pad)

    def _dispatch(self, callback: Callable[[], None]) -> None:
        self.after(0, callback)

    def _browse_input(self) -> None:
        try:
            from tkinter import filedialog
        except Exception:
            return

        folder = filedialog.askdirectory(title="Select input folder")
        if not folder:
            return

        path = Path(folder)
        self.input_path.set(str(path))
        self._update_output_preview(path)

    def _update_output_preview(self, input_dir: Path) -> None:
        try:
            output_dir = plan_output_dir(input_dir)
        except Exception as exc:
            self.output_path.set("(error)")
            self.status_text.set(f"Output planning failed: {exc}")
            return

        self.output_path.set(str(output_dir))

    def _run_conversion(self) -> None:
        input_value = self.input_path.get()
        if not input_value or input_value == "(not selected)":
            self._show_message("Input folder is required.", kind="warning")
            return

        input_dir = Path(input_value)
        self.status_text.set("Preparing conversion...")
        self.progress_bar.configure(value=0)
        self._set_controls_enabled(False)

        if not self.controller.start(input_dir):
            self._set_controls_enabled(True)
            self._show_message("Conversion is already running.", kind="warning")

    def _set_controls_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.input_button.configure(state=state)
        self.run_button.configure(state=state)

    def _on_start(self, output_dir: Path, total: int) -> None:
        self.output_path.set(str(output_dir))
        self.progress_bar.configure(maximum=max(total, 1), value=0)
        if total == 0:
            self.status_text.set("No files found.")
        else:
            self.status_text.set("Starting conversion...")

    def _on_progress(self, event: ProgressEvent) -> None:
        self.progress_bar.configure(maximum=max(event.total, 1), value=event.index)
        self.status_text.set(
            f"{event.index}/{event.total}: {event.current_file.name}"
        )

    def _on_complete(self, summary: ConversionSummary) -> None:
        self._set_controls_enabled(True)
        if summary.total == 0:
            self.status_text.set("Completed (no files).")
        else:
            self.status_text.set("Completed.")

        message = (
            "変換が完了しました。\n\n"
            f"成功: {summary.success_count}\n"
            f"失敗: {summary.failure_count}\n"
            f"出力先: {summary.output_dir}\n"
            f"ログ: {summary.log_path}"
        )
        self._show_message(message, kind="info")

    def _on_error(self, error: Exception) -> None:
        self._set_controls_enabled(True)
        self.status_text.set("Error.")
        self._show_message(f"変換に失敗しました: {error}", kind="error")

    def _show_message(self, message: str, kind: str = "info") -> None:
        try:
            from tkinter import messagebox
        except Exception:
            return

        if kind == "error":
            messagebox.showerror("Error", message, parent=self.master)
        elif kind == "warning":
            messagebox.showwarning("Warning", message, parent=self.master)
        else:
            messagebox.showinfo("Info", message, parent=self.master)
