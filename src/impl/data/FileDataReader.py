from io import TextIOWrapper
from dataclasses import dataclass, field
from pathlib import Path
from typing import LiteralString, Any
import numpy as np

from src.api.data import DataReader


@dataclass
class FileDataReader(DataReader[np.ndarray]):
    path: Path | str
    sep: LiteralString = field(default=";")
    names: bool = field(default=False)
    file: TextIOWrapper | None = field(default=None, init=False)

    def _open_resource(self) -> None:
        file_path = Path(self.path)
        if not file_path.is_file():
            raise FileNotFoundError(f"Файл не найден по пути: {self.path}")

        self.file = open(self.path, "r", encoding="utf-8-sig")

    def _close_resource(self) -> None:
        if self.file is not None:
            self.file.close()

    def read_data(self) -> np.ndarray[tuple[Any, ...], np.dtype[Any]]:
        if self.file is None:
            raise RuntimeError("Файл не открыт. Используйте контекстный менеджер 'with'.")
        if len(self.file.read(1)) == 0:
            raise ValueError("Файл пустой.")
        self.file.seek(0)

        data = []
        for line in self.file:
            line = line.encode("cp1251").decode("utf-8")
            data.append(line)

        return np.genfromtxt(
            data,
            delimiter=self.sep,
            dtype=None,
            names=True if self.names else None,
            encoding="utf-8",
        )