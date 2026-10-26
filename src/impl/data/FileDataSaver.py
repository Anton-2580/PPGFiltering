from dataclasses import dataclass, field
from io import TextIOWrapper
from pathlib import Path
from typing import LiteralString
import numpy as np

from src.api.data import DataSaver


@dataclass
class FileDataSaver(DataSaver[np.ndarray[tuple[int]]]):
    path: Path | str
    fmt: str = field(default="%s")
    sep: LiteralString = field(default=";")
    file: TextIOWrapper | None = field(default=None, init=False)

    def _open_resource(self) -> None:
        self.file = open(self.path, "w", encoding="utf-8")

    def _close_resource(self) -> None:
        if self.file is not None:
            self.file.close()

    def save_data(self, data: np.ndarray[tuple[int]]) -> None:
        if self.file is None:
            raise RuntimeError("Файл не открыт. Используйте контекстный менеджер 'with'.")

        np.savetxt(self.file, data, delimiter=self.sep, newline="\n", fmt=self.fmt)
