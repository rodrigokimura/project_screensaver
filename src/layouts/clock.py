import time
from tkinter import BOTH, Frame, Label, Misc
from tkinter.font import Font
from typing import Tuple

from .base import TkinterLayout


class Clock(TkinterLayout):
    def __init__(self, bg: str) -> None:
        self.bg = bg

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)

        self.font = Font(family="Cascadia Code")
        self.font.config(size=100)

        self.frame = Frame(self.window)

        self.label = Label(self.frame, text="", fg="white", bg=self.bg, font=self.font)
        self.label.pack(fill=BOTH, expand=1)

        self.window.configure(bg=self.bg)
        self.frame.configure(bg=self.bg)
        self.frame.pack_forget()

        self._adjust_size(size)
        self._update_clock()

    def _adjust_size(self, display_size):
        w, h = display_size
        w = 0.7 * w

        proportion = self.font.metrics("linespace") / self.font.measure("00:00:00")
        h = w * proportion
        self.font.config(size=-int(h))

        self.frame.pack(expand=1)

    def _update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.window.after(1000, self._update_clock)
