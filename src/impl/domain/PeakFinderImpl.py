import numpy as np

from src.api.domain import PeakFinder


class PeakFinderImpl(PeakFinder):
    def search_with_std(self, data: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.ndarray[tuple[int], np.dtype[np.integer]]:
        count = round(self.Hz * self.refractory_period)
        peak_indexes = []

        i = 1
        threshold = self.threshold * data.std()
        while i < data.shape[0] - 1:
            elem = data[i]
            if elem > threshold and data[i - 1] < elem > data[i + 1]:
                window_end = min(i + count, data.shape[0])
                window = data[i:window_end]

                local_max_idx = np.argmax(window)

                if local_max_idx == 0:
                    peak_indexes.append(i)
                    i += count
                else:
                    i += int(local_max_idx)
            else:
                i += 1

        return np.array(peak_indexes)