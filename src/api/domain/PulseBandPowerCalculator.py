from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np


@dataclass
class PulseBandPowerCalculator(ABC):
    Hz: float | int

    @abstractmethod
    def calc(self, data: np.ndarray) -> np.number: ...