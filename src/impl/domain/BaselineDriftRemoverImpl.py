import numpy as np

from src.api.domain import BaselineDriftRemover


class BaselineDriftRemoverImpl(BaselineDriftRemover):
    def remove_baseline_drift(self, data: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        count = round(self.Hz * self.time)
        if count % 2 == 0: count += 1

        filtered_data = self.filter(N=count).filter(data)
        result = data - filtered_data
        return result.astype(np.float64)