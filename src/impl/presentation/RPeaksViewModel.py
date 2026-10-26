import numpy as np

from src.api.presentation.ViewModel import ViewModel


class RPeaksViewModel(ViewModel):
    @staticmethod
    def get_bpm(timestamps: np.ndarray[tuple[int], np.dtype[np.number]]) -> np.ndarray[tuple[int], np.dtype[np.number]]:
        intervals = np.diff(timestamps)
        bpm = 60.0 / intervals
        return bpm