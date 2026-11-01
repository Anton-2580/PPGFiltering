import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from main import main


class TestFiles(unittest.TestCase):

    @patch("builtins.input", side_effect=["75", "0.1"])
    @patch("pathlib.Path.resolve")
    def test_absence_of_files(self, mock_path: MagicMock, mock_input: MagicMock) -> None:
        mock_path.side_effect = lambda: Path(__file__)

        f = io.StringIO()
        with redirect_stdout(f):
            main()

        self.assertRegex(f.getvalue(), "^Файл не найден по пути: .+\n$")

    @patch("builtins.input", side_effect=["75", "0.1"])
    def test_empty_file(self, mock_input: MagicMock) -> None:
        with patch("builtins.open", mock_open(read_data="")):
            f = io.StringIO()
            with redirect_stdout(f):
                main()

            self.assertEqual(f.getvalue(), "Файл пустой.\n")

    @patch("builtins.input", side_effect=["75", "0.1"])
    def test_invalid_file_datatype(self, mock_input: MagicMock) -> None:
        bad_data = """
            0.123
            0.234
            hi
        """
        with patch("builtins.open", mock_open(read_data=bad_data)):
            f = io.StringIO()
            with redirect_stdout(f):
                main()

            self.assertRegex(f.getvalue(), r"^Формат файла не совпадает по типам колонок. \(dtype .+\)\n$")


if __name__ == "__main__":
    unittest.main()