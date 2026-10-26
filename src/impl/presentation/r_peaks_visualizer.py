from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt

from src.impl.presentation.RPeaksViewModel import RPeaksViewModel


def r_peaks_visualizer(
    timestamps_list: Sequence[np.ndarray[tuple[int], np.dtype[np.number]]],
    titles: Sequence[str],
    view_model: RPeaksViewModel = RPeaksViewModel(),
) -> None:
    fig, ax = plt.subplots(1, len(timestamps_list), figsize=(6*len(timestamps_list), 8))
    axes = np.atleast_1d(ax)

    for index, timestamps in enumerate(timestamps_list):
        bpm = view_model.get_bpm(timestamps)
        axes[index].set_title(titles[index])
        axes[index].plot(bpm, "o-", color="red", markersize=4, label="Пульс (ЧСС)")
        axes[index].set_ylabel("Удары в минуту (BPM)")
        axes[index].set_xlabel("Номер сердечного сокращения")
        axes[index].legend()

    fig.tight_layout()
    plt.show()