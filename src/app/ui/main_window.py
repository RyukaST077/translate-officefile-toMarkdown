"""Main application window UI skeleton."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class MainWindow(ttk.Frame):
    """Minimal Tkinter UI layout without behavior wiring."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=12)
        self.master = master

        self.input_path = tk.StringVar(value="(not selected)")
        self.output_path = tk.StringVar(value="(auto-generated)")
        self.status_text = tk.StringVar(value="Idle")

        self._build_layout()

    def _build_layout(self) -> None:
        self.grid(row=0, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.columnconfigure(1, weight=1)

        input_label = ttk.Label(self, text="Input folder")
        input_entry = ttk.Entry(self, textvariable=self.input_path, state="readonly")
        input_button = ttk.Button(self, text="Browse")

        output_label = ttk.Label(self, text="Output folder")
        output_entry = ttk.Entry(self, textvariable=self.output_path, state="readonly")

        run_button = ttk.Button(self, text="Run")

        self.progress_bar = ttk.Progressbar(self, mode="determinate")
        status_label = ttk.Label(self, textvariable=self.status_text)

        pad = {"padx": 6, "pady": 6}
        input_label.grid(row=0, column=0, sticky="w", **pad)
        input_entry.grid(row=0, column=1, sticky="ew", **pad)
        input_button.grid(row=0, column=2, sticky="e", **pad)

        output_label.grid(row=1, column=0, sticky="w", **pad)
        output_entry.grid(row=1, column=1, columnspan=2, sticky="ew", **pad)

        run_button.grid(row=2, column=0, columnspan=3, sticky="ew", **pad)

        self.progress_bar.grid(row=3, column=0, columnspan=3, sticky="ew", **pad)
        status_label.grid(row=4, column=0, columnspan=3, sticky="w", **pad)
