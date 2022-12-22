from tkinter import Tk, Toplevel
from typing import List, Union

from layouts import Calendar, Clock, Layout, SolidColor
from utils import get_display_sizes_and_position


class Screensaver:

    displays: List[Union[Tk, Toplevel]]
    layouts: List[Layout]

    def __init__(self, layouts: List[Layout]):
        self.layouts = layouts
        self.configure()

    def configure(self):
        self.tk = Tk()
        self.tk.withdraw()

        displays = get_display_sizes_and_position()

        for i, display in enumerate(displays):
            layout = self.layouts[i]
            layout.configure(
                self.tk, (display.width, display.height), (display.x, display.y)
            )

    def start(self):
        self.tk.mainloop()


if __name__ == "__main__":
    w = Screensaver(layouts=[SolidColor("black"), Clock(), Calendar()])
    w.start()
