from abc import ABC, abstractmethod
from tkinter import Misc, TclError, Toplevel
from typing import Tuple


class Layout(ABC):
    @abstractmethod
    def configure(self, *args, **kwargs):
        ...

    @abstractmethod
    def destroy(self):
        ...


class TkinterLayout(Layout):
    window: Toplevel

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        self.window = Toplevel(master)
        w, h = size
        x, y = position
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        self.window.config(cursor="none")
        self.window.attributes("-fullscreen", True)
        self.window.bind("<Escape>", self.destroy)

    def destroy(self, event=None):
        try:
            self.window.master.destroy()
            self.window.destroy()
        except TclError:
            pass
