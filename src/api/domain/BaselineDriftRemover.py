from abc import abstractmethod, ABC
from dataclasses import dataclass
import numpy as np

from src.api.domain.filters import FilterWithWindow


@dataclass
class BaselineDriftRemover(ABC):
    filter: type[FilterWithWindow]
    time: float
    Hz: float | int

    @abstractmethod
    def remove_baseline_drift(self, data: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.ndarray[tuple[int], np.dtype[np.number]]: ...