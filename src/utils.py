import os
import re
from typing import Dict, List, NamedTuple, Tuple


class Display(NamedTuple):
    width: int
    height: int
    x: int
    y: int


def get_all_monitors_resolution() -> List[Tuple[int, int]]:
    cli_result = os.popen("xrandr | grep '*'").read()
    resolutions = [s.strip().split(" ")[0] for s in cli_result.split("\n")]
    return [
        (int(r.split("x")[0]), int(r.split("x")[1])) for r in resolutions if r != ""
    ]


def get_display_sizes_and_position() -> List[Display]:

    # {width}x{height}+{pos_x}+{pos_y} -> 1920x1080+0+0
    pattern = re.compile(r"(\d+)x(\d+)\+(\d+)\+(\d+)")

    cli_result = os.popen("xrandr | grep ' connected'").read()
    result = re.findall(pattern, cli_result)

    return [Display(*[int(i) for i in r]) for r in result]
