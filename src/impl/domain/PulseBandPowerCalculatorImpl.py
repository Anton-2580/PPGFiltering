import numpy as np

from src.api.domain import PulseBandPowerCalculator


class PulseBandPowerCalculatorImpl(PulseBandPowerCalculator):
    def calc(self, data: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.floating:
        res_data = data - np.mean(data)

        f_total = np.arange(0.2, 15.01, 0.05)
        f_useful = np.arange(0.7, 3.01, 0.05)

        total: np.floating = np.sum([self.A(res_data, f) for f in f_total])
        useful: np.floating = np.sum([self.A(res_data, f) for f in f_useful])

        return useful / total

    def A(self, data: np.ndarray[tuple[int]], f: np.floating) -> np.floating:
        if not 0.2 <= f <= 15:
            raise ValueError("Частота вне диапазона")

        i = np.arange(data.shape[0])
        res: np.floating = (
            np.sum(data * np.cos(2 * np.pi * f * i / self.Hz)) ** 2 +
            np.sum(data * np.sin(2 * np.pi * f * i / self.Hz)) ** 2
        )
        return res