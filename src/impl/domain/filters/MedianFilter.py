from dataclasses import dataclass
import numpy as np

from src.api.domain import FilterWithWindow, BaseSorter


@dataclass
class MedianFilter(FilterWithWindow):
    sorter: type[BaseSorter[tuple[int], np.dtype[np.number]]] | BaseSorter[tuple[int], np.dtype[np.number]]

    def filter(
        self,
        data: np.ndarray[tuple[int], np.dtype[np.number]]
    ) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        size = data.shape[0]
        res = np.zeros_like(data)

        k = self.N // 2
        for i in range(size):
            start = i - k if i - k > 0 else 0
            end = i + k + 1 if i + k + 1 < size else size

            sorted_data = self.sorter.sort(data[start:end].copy())
            l = len(sorted_data) // 2
            if len(sorted_data) % 2 == 1:
                res[i] = sorted_data[l]
            else:
                res[i] = np.mean(sorted_data[l - 1:l + 1])

        return res