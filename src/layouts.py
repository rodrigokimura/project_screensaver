import datetime
import time
from abc import ABC, abstractmethod
from tkinter import BOTH, Frame, Label, Misc, TclError, Toplevel
from tkinter.font import Font
from typing import List, Tuple


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
    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)

        self.font = Font(family="Cascadia Code")
        self.font.config(size=100)

        self.frame = Frame(self.window)

        self.label = Label(self.frame, text="", fg="white", bg="black", font=self.font)
        self.label.pack(fill=BOTH, expand=1)

        self.window.configure(bg="black")
        self.frame.configure(bg="black")
        self.frame.pack_forget()

        self.window.after(500, self._adjust_size)
        self.window.after(100, self._update_clock)

    def _adjust_size(self):
        w, h = self.window.winfo_width(), self.window.winfo_height()
        w = 0.7 * w

        proportion = self.font.metrics("linespace") / self.font.measure("00:00:00")
        h = w * proportion
        self.font.config(size=-int(h))

        self.frame.pack(expand=1)

    def _update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.window.after(1000, self._update_clock)


class Calendar(TkinterLayout):
    labels: List[Label] = []

    def configure(self, master: Misc, size: Tuple[int, int], position: Tuple[int, int]):
        super().configure(master, size, position)

        self.font = Font(family="Cascadia Code")
        self.font.config(size=100)

        self.frame = Frame(self.window)

        self._populate_calendar()

        self.frame.configure(bg="black")
        self.frame.pack_forget()

        self.window.configure(bg="black")
        self.window.after(100, self._adjust_size)

    def _populate_calendar(self):

        first_day_of_month = self._get_first_day_of_month()
        first_date_to_display = first_day_of_month - datetime.timedelta(
            days=self._get_weekday(first_day_of_month)
        )

        for i in range(5 * 7):
            c = i % 7
            r = i // 7
            date = first_date_to_display + datetime.timedelta(days=i)
            l = self._date_label(str(date.day))
            l.grid(row=r, column=c, padx=0, pady=0)
            if date.month != first_day_of_month.month:
                l.configure(fg="grey")
            if date == datetime.date.today():
                l.configure(fg="red")
            self.labels.append(l)

    def _get_weekday(self, date: datetime.date):
        return date.weekday()

    def _get_first_day_of_month(self):
        today = datetime.date.today()
        first = today.replace(day=1)
        return first

    def _date_label(self, text: str):
        return Label(
            self.frame,
            text=text,
            fg="white",
            bg="black",
            font=self.font,
            width=2,
        )

    def _adjust_size(self):
        h = self.window.winfo_height() * 0.7 / 2 / 5
        self.font.config(size=-int(h))
        self.frame.pack(expand=1)
        for l in self.labels:
            l.configure(padx=h / 2, pady=h / 2)
