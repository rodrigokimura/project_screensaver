import math
import time
from itertools import product
from tkinter import BOTH, Canvas, Frame, Label, Misc
from tkinter.font import Font
from typing import Tuple

from .base import TkinterLayout


class DigitalClock(TkinterLayout):
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


class AnalogClock(TkinterLayout):

    HOUR_TICKS = 12
    MINUTE_TICKS_BY_HOUR = 5
    SUBTICKS_BY_TICK = 4

    def __init__(self, bg: str) -> None:
        self.bg = bg
        self.padding = 100
        self.hour_handle = None
        self.minute_handle = None
        self.second_handle = None
        self.hour_angle_inc = 360 / self.HOUR_TICKS
        self.minute_angle_inc = 360 / (self.HOUR_TICKS * self.MINUTE_TICKS_BY_HOUR)
        self.subtick_angle_inc = 360 / (
            self.HOUR_TICKS * self.MINUTE_TICKS_BY_HOUR * self.SUBTICKS_BY_TICK
        )

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)
        self.diameter = self._get_diameter(size)
        self.center = (size[0] // 2, size[1] // 2)
        self._draw_clock(size)
        self._update_clock()

    def _draw_clock(self, size: Tuple[int, int]):
        self.cv = Canvas(
            self.window,
            width=size[0],
            height=size[1],
            bg=self.bg,
            borderwidth=0,
            highlightthickness=0,
        )
        self.cv.pack(fill=BOTH, expand=1)

        # self._draw_dial()
        self._draw_center(20)
        self._draw_ticks()

    def _get_diameter(self, size: Tuple[int, int]) -> int:
        return min(size[0], size[1]) - self.padding

    def _draw_dial(self):
        x, y = self.center
        self.cv.create_oval(
            x - self.diameter // 2,
            y - self.diameter // 2,
            x + self.diameter // 2,
            y + self.diameter // 2,
            width=10,
            outline="gray",
            fill=self.bg,
        )

    def _draw_center(self, size: int):
        color = "gray"
        x, y = self.center
        self.cv.create_oval(
            x - size // 2,
            y - size // 2,
            x + size // 2,
            y + size // 2,
            fill=color,
            outline=color,
        )

    def _draw_ticks(self):
        for (h, m, s) in product(
            range(self.HOUR_TICKS),
            range(self.MINUTE_TICKS_BY_HOUR),
            range(self.SUBTICKS_BY_TICK),
        ):
            angle = (
                h * self.hour_angle_inc
                + m * self.minute_angle_inc
                + s * self.subtick_angle_inc
            )

            is_hour = m == 0 and s == 0
            is_minute = s == 0

            if is_hour:
                self._draw_tick(angle, 0.85, width=5)
            elif is_minute:
                self._draw_tick(angle, 0.9, width=3)
            else:
                self._draw_tick(angle, 0.95, width=1)

    def _draw_tick(
        self,
        angle: float,
        start: float,
        end: float = 1,
        width: int = 3,
        color: str = "gray",
    ):
        angle = math.radians(angle)
        x, y = self.center
        r = (self.diameter // 2) * end
        x1 = x + start * r * math.sin(angle)
        y1 = y - start * r * math.cos(angle)
        x2 = x + r * math.sin(angle)
        y2 = y - r * math.cos(angle)
        return self.cv.create_line(x1, y1, x2, y2, width=width, fill=color)

    def _draw_handles(self):
        self._draw_hour_handle()
        self._draw_minute_handle()
        self._draw_second_handle()

    def _draw_hour_handle(self):
        if self.hour_handle:
            self.cv.delete(self.hour_handle)
        hour = time.strftime("%H")
        angle = (360 / 12) * int(hour)
        self.hour_handle = self._draw_tick(angle, 0, 0.6, width=10, color="white")

    def _draw_minute_handle(self):
        if self.minute_handle:
            self.cv.delete(self.minute_handle)
        minute = time.strftime("%M")
        angle = (360 / 60) * int(minute)
        self.minute_handle = self._draw_tick(angle, 0, 0.8, width=10, color="white")

    def _draw_second_handle(self):
        if self.second_handle:
            self.cv.delete(self.second_handle)

        milis = time.time_ns() // 1_000_000

        angle = (360 / 60) * (milis / 1000) - self.subtick_angle_inc * 2.5

        self.second_handle = self._draw_tick(angle, 0, 0.8, width=1, color="red")

    def _update_clock(self):
        self._draw_handles()
        self.window.after(10, self._update_clock)
