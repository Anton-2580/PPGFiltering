from abc import ABC, abstractmethod

import numpy as np


class BaseSorter[Shape: tuple[int], Dtype: np.dtype](ABC):
    @staticmethod
    @abstractmethod
    def sort(
        data: np.ndarray[Shape, Dtype]
    ) -> np.ndarray[Shape, Dtype]: ...