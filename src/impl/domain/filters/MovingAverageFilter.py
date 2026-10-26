import numpy as np

from src.api.domain import FilterWithWindow


class MovingAverageFilter(FilterWithWindow):
    def filter(
        self,
        data: np.ndarray[tuple[int], np.dtype[np.number]]
    ) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        res = np.zeros_like(data)
        size = data.shape[0]
        k = self.N // 2

        for i in range(size):
            start = i - k if i - k > 0 else 0
            end = i + k + 1 if i + k + 1 < size else size

            res[i] = np.mean(data[start:end])

        return res