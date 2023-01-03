from tkinter import Misc
from typing import Tuple

from .base import TkinterLayout


class SolidColor(TkinterLayout):
    def __init__(self, color) -> None:
        self._color = color
        super().__init__()

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)
        self.window.configure(bg=self._color)
