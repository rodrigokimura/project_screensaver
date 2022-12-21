import contextlib
from unittest.mock import Mock, patch

from utils import Display, get_all_monitors_resolution, get_display_sizes_and_position


class TestGetAllMonitorsResolution:
    @contextlib.contextmanager
    def simulate_monitors(self, count: int = 1):
        FAKE_RETURN = "   1920x1080     60.00*+  74.97    50.00    59.94"
        with patch("os.popen") as mocked_popen:
            process_mock = Mock()
            attrs = {"read.return_value": "\n".join([FAKE_RETURN] * count)}
            process_mock.configure_mock(**attrs)
            mocked_popen.return_value = process_mock
            yield

    def test_one_monitor(self):
        with self.simulate_monitors():
            result = get_all_monitors_resolution()
        assert result == [(1920, 1080)]

    def test_two_monitors(self):
        with self.simulate_monitors(2):
            result = get_all_monitors_resolution()
        assert result == [(1920, 1080)] * 2

    def test_three_monitors(self):
        with self.simulate_monitors(3):
            result = get_all_monitors_resolution()
        assert result == [(1920, 1080)] * 3


class TestGetDisplaySizesAndPosition:

    ONE_DISPLAY = "DisplayPort-0 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 480mm x 270mm"

    TWO_DISPLAYS = """DisplayPort-0 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 480mm x 270mm
        HDMI-A-0 connected 1920x1080+1920+0 (normal left inverted right x axis y axis) 480mm x 270mm"""

    THREE_DISPLAYS = """DisplayPort-0 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 480mm x 270mm
        HDMI-A-0 connected 1920x1080+1920+0 (normal left inverted right x axis y axis) 480mm x 270mm
        DVI-D-0 connected 1920x1080+3840+0 (normal left inverted right x axis y axis) 480mm x 270mm
        """

    @contextlib.contextmanager
    def simulate_monitors(self, count: int = 1):
        fake_return = {
            1: self.ONE_DISPLAY,
            2: self.TWO_DISPLAYS,
            3: self.THREE_DISPLAYS,
        }.get(count, self.ONE_DISPLAY)

        with patch("os.popen") as mocked_popen:
            process_mock = Mock()
            attrs = {"read.return_value": fake_return}
            process_mock.configure_mock(**attrs)
            mocked_popen.return_value = process_mock
            yield

    def test_one_monitor(self):
        with self.simulate_monitors():
            result = get_display_sizes_and_position()
        assert result == [
            Display(1920, 1080, 0, 0),
        ]

    def test_two_monitors(self):
        with self.simulate_monitors(2):
            result = get_display_sizes_and_position()
        assert result == [
            Display(1920, 1080, 0, 0),
            Display(1920, 1080, 1920, 0),
        ]

    def test_three_monitors(self):
        with self.simulate_monitors(3):
            result = get_display_sizes_and_position()
        assert result == [
            Display(1920, 1080, 0, 0),
            Display(1920, 1080, 1920, 0),
            Display(1920, 1080, 3840, 0),
        ]
