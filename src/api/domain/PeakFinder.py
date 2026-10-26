from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import numpy as np


@dataclass
class PeakFinder(ABC):
    refractory_period: float
    Hz: float | int
    threshold: float = field(default=0.5)

    @abstractmethod
    def search_with_std(self, data: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.ndarray[tuple[int], np.dtype[np.integer]]: ...