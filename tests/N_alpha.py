import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch, MagicMock

from main import main


class TestNAlphaOutOfTheRange(unittest.TestCase):

    @patch("builtins.input", side_effect=["2", "0"])
    def test_N(self, mock_input: MagicMock) -> None:
        f = io.StringIO()
        with redirect_stdout(f):
            main()

        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(f.getvalue(), "N должно быть нечетным числом.\n")

    @patch("builtins.input", side_effect=["21", "1.1"])
    def test_alpha(self, mock_input: MagicMock) -> None:
        f = io.StringIO()
        with redirect_stdout(f):
            main()

        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(f.getvalue(), "значении альфа вне диапазона от 0 до 1.\n")

    @patch("main.get_r_peaks", return_value=...)
    @patch("main.get_files", return_value=[[[..., 20]]])
    @patch("builtins.input", side_effect=["75", "0.1"])
    def test_N_bigger_window_size(self, mock_input: MagicMock, mock_files: MagicMock, mock_r_peaks: MagicMock) -> None:
        f = io.StringIO()
        with redirect_stdout(f):
            main()

        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(f.getvalue(), "N не может быть больше длины записи.\n")


if __name__ == "__main__":
    unittest.main()