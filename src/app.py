import sys
from tkinter import Frame, Tk, Toplevel
from typing import List, Union

from utils import get_display_sizes_and_position


class Screensaver:

    windows: List[Union[Tk, Toplevel]]
    state: bool

    def __init__(self):
        self.state = False
        self.render()
        self.bind_keys()
        self.hide_cursor()
        self.toggle_fullscreen()

    def bind_keys(self):
        for window in self.windows:
            window.bind("<Escape>", self.exit)

    def render(self):
        displays = get_display_sizes_and_position()
        main_monitor = displays.pop()

        self.tk = Tk()
        self.tk.attributes("-zoomed", True)
        self.tk.geometry(
            f"{main_monitor.width}x{main_monitor.height}+{main_monitor.x}+{main_monitor.y}"
        )

        self.frame = Frame(self.tk)
        self.frame.pack()

        self.windows = [self.tk]

        for display in displays:
            new_window = self.render_extra_monitor(
                (display.width, display.height), (display.x, display.y)
            )
            self.windows.append(new_window)
        
        for window in self.windows:
            window.configure(bg='black')

    def render_extra_monitor(self, size, position):
        new_window = Toplevel(self.tk)
        new_window.title("New Window")
        w, h = size
        x, y = position
        new_window.geometry(f"{w}x{h}+{x}+{y}")
        return new_window

    def hide_cursor(self):
        for window in self.windows:
            window.config(cursor="none")

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        for window in self.windows:
            window.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        for window in self.windows:
            window.attributes("-fullscreen", False)
        return "break"

    def exit(self, event=None):
        self.tk.destroy()
        sys.exit()

    def start(self):
        self.tk.mainloop()


if __name__ == "__main__":
    w = Screensaver()
    w.start()
