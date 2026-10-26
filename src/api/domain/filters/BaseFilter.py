from abc import ABC, abstractmethod

import numpy as np


class BaseFilter[Shape: tuple[int, ...], Dtype: np.dtype](ABC):
    @abstractmethod
    def filter(
        self,
        data: np.ndarray[Shape, Dtype]
    ) -> np.ndarray[Shape, Dtype]: ...
