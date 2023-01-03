from unittest.mock import MagicMock, patch

from layouts.calendar import Calendar, Date


class TestCalendar:
    c = Calendar("black")

    @patch("layouts.calendar.Date")
    def test_get_first_date_to_display_when_sunday(self, mock_date: MagicMock):
        mock_date.today.return_value = Date(2023, 1, 2)
        mock_date.side_effect = lambda *args, **kw: Date(*args, **kw)
        assert self.c._get_first_date_to_display() == Date(2023, 1, 1)

    @patch("layouts.calendar.Date")
    def test_get_first_date_to_display_when_not_sunday(self, mock_date: MagicMock):
        mock_date.today.return_value = Date(2023, 2, 2)
        mock_date.side_effect = lambda *args, **kw: Date(*args, **kw)
        assert self.c._get_first_date_to_display() == Date(2023, 1, 29)

    @patch("layouts.calendar.Date")
    def test_get_first_day_of_month(self, mock_date: MagicMock):
        mock_date.today.return_value = Date(2023, 2, 2)
        mock_date.side_effect = lambda *args, **kw: Date(*args, **kw)
        assert self.c._get_first_day_of_month() == Date(2023, 2, 1)
