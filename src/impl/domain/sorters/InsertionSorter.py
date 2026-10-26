import numpy as np

from src.api.domain import BaseSorter


class InsertionSorter(BaseSorter[tuple[int], np.dtype[np.number]]):
    @staticmethod
    def sort(
        data: np.ndarray[tuple[int], np.dtype[np.number]]
    ) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        for index in range(1, len(data)):
            key = data[index]
            j = index - 1
            while j >= 0 and data[j] > key:
                j -= 1
            data[j+2:index+1] = data[j+1:index]
            data[j+1] = key

        return data
