from abc import ABC
from dataclasses import dataclass
import numpy as np

from .BaseFilter import BaseFilter


@dataclass
class FilterWithAlpha(BaseFilter[tuple[int], np.dtype[np.number]], ABC):
    alpha: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError("значении альфа вне диапазона от 0 до 1.")