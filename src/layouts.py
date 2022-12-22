import time
from abc import ABC, abstractmethod
from tkinter import BOTH, Frame, Label, Misc, TclError, Toplevel
from tkinter.font import Font
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


class SolidColor(TkinterLayout):
    def __init__(self, color) -> None:
        self._color = color
        super().__init__()

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)
        self.window.configure(bg=self._color)


class Clock(TkinterLayout):
    def __init__(self) -> None:
        super().__init__()

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)

        self.font = Font(family="Cascadia Code")

        f = Frame(self.window)
        f.pack(fill=BOTH, expand=1)
        f.configure(bg="black")

        self.font.config(size=100)
        self.label = Label(f, text="...", fg="white", bg="black", font=self.font)

        self.label.pack(fill=BOTH, expand=1)
        self.window.configure(bg="black")

        self.window.after(1000, self._adjust_size)
        self.window.after(1000, self._update_clock)

    def _adjust_size(self):
        w, h = self.window.winfo_width(), self.window.winfo_height()
        w = 0.8 * w
        fits = False
        while not fits:
            self.font.config(size=int(h))
            if self.font.measure("00:00:00") > w:
                h -= 10
            else:
                fits = True

        self.label.configure(font=self.font)

    def _update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.window.after(1000, self._update_clock)
