import enum
from datetime import date, timedelta
from tkinter import Frame, Label, Misc
from tkinter.font import Font
from typing import List, Tuple

from .base import TkinterLayout


class Weekday(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Date(date):
    def weekday(self) -> Weekday:
        return Weekday[self.strftime("%A").upper()]


class Calendar(TkinterLayout):
    labels: List[Label] = []

    def __init__(self, bg: str) -> None:
        self.bg = bg

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)

        self.font = Font(family="Cascadia Code")
        self.font.config(size=100)

        self.frame = Frame(self.window)

        self._populate_calendar()

        self.frame.configure(bg=self.bg)
        self.frame.pack_forget()

        self.window.configure(bg=self.bg)
        self._adjust_size(size)

    def _populate_calendar(self):

        first_day_of_month = self._get_first_day_of_month()
        current_month = first_day_of_month.month
        first_date_to_display = self._get_first_date_to_display()

        for i in range(5 * 7):
            c = i % 7
            r = i // 7
            dt = first_date_to_display + timedelta(days=i)
            l = self._date_label(str(dt.day))
            l.grid(row=r, column=c, padx=0, pady=0)
            if dt.weekday() == Weekday.SUNDAY:
                l.configure(fg="red")
            if dt.weekday() == Weekday.SATURDAY:
                l.configure(fg="grey")
            if dt.month != current_month:
                l.configure(fg="grey")
            if dt == date.today():
                l.configure(fg="black", bg="white")
            self.labels.append(l)

    def _get_first_day_of_month(self) -> Date:
        today = Date.today()
        first = today.replace(day=1)
        return first

    def _get_first_date_to_display(self):
        first_day_of_month = self._get_first_day_of_month()
        if first_day_of_month.weekday() == Weekday.SUNDAY:
            return first_day_of_month
        return first_day_of_month - timedelta(
            days=first_day_of_month.weekday().value + 1
        )

    def _date_label(self, text: str):
        return Label(
            self.frame,
            text=text,
            fg="white",
            bg=self.bg,
            font=self.font,
            width=2,
        )

    def _adjust_size(self, display_size):
        _, h = display_size
        h = h * 0.7 / 2 / 5
        self.font.config(size=-int(h))
        self.frame.pack(expand=1)
        for l in self.labels:
            l.configure(padx=h / 2, pady=h / 2)
