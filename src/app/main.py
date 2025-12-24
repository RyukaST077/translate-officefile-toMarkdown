"""Application entry point."""

from __future__ import annotations

import os
import sys
import types


def _has_display() -> bool:
    if sys.platform.startswith("win"):
        return True
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _install_tkinter_stub() -> None:
    class _DummyWidget:
        def __init__(self, *args, **kwargs) -> None:
            self.master = kwargs.get("master")

        def grid(self, *args, **kwargs) -> None:
            return None

        def columnconfigure(self, *args, **kwargs) -> None:
            return None

        def rowconfigure(self, *args, **kwargs) -> None:
            return None

        def title(self, *args, **kwargs) -> None:
            return None

        def geometry(self, *args, **kwargs) -> None:
            return None

        def minsize(self, *args, **kwargs) -> None:
            return None

        def mainloop(self, *args, **kwargs) -> None:
            return None

    class _DummyFrame(_DummyWidget):
        pass

    class _DummyStringVar:
        def __init__(self, value: str = "") -> None:
            self._value = value

        def get(self) -> str:
            return self._value

        def set(self, value: str) -> None:
            self._value = value

    tk_stub = types.ModuleType("tkinter")
    ttk_stub = types.ModuleType("tkinter.ttk")

    tk_stub.Tk = _DummyWidget
    tk_stub.StringVar = _DummyStringVar
    tk_stub.ttk = ttk_stub

    ttk_stub.Frame = _DummyFrame
    ttk_stub.Label = _DummyWidget
    ttk_stub.Entry = _DummyWidget
    ttk_stub.Button = _DummyWidget
    ttk_stub.Progressbar = _DummyWidget

    sys.modules.setdefault("tkinter", tk_stub)
    sys.modules.setdefault("tkinter.ttk", ttk_stub)


def _prepare_tkinter() -> "types.ModuleType":
    if not _has_display():
        _install_tkinter_stub()
        import tkinter as tk
        return tk
    try:
        import tkinter as tk
        return tk
    except ModuleNotFoundError:
        _install_tkinter_stub()
        import tkinter as tk
        return tk


def main() -> None:
    tk = _prepare_tkinter()

    from app.config import DEFAULT_WINDOW_SIZE, WINDOW_TITLE
    from app.ui.main_window import MainWindow

    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry(DEFAULT_WINDOW_SIZE)
    root.minsize(640, 360)

    MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()
