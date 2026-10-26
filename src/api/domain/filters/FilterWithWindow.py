from abc import ABC
from dataclasses import dataclass
import numpy as np

from .BaseFilter import BaseFilter


@dataclass
class FilterWithWindow(BaseFilter[tuple[int], np.dtype[np.number]], ABC):
    N: int

    def __post_init__(self) -> None:
        if self.N % 2 == 0:
            raise ValueError("N должно быть нечетным числом.")

    def check_window_size(self, length: int) -> None:
        if length < self.N:
            raise ValueError("N не может быть больше длины записи.")