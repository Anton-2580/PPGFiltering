import numpy as np

from src.api.domain import FilterWithAlpha


class ExponentialSmoothingFilter(FilterWithAlpha):
    def filter(
        self,
        data: np.ndarray[tuple[int], np.dtype[np.number]]
    ) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        res = np.zeros_like(data)
        res[0] = data[0]

        for i in range(1, len(data)):
            res[i] = self.alpha * data[i] + (1 - self.alpha) * res[i - 1]

        return res