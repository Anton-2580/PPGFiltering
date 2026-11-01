from typing import Sequence
import matplotlib.pyplot as plt
import numpy as np


def filter_visualizer(
    compare_datas: Sequence[np.ndarray],
    filtering_datas: Sequence[np.ndarray],
    filtered_datas: np.ndarray[tuple[int, int, int], np.dtype[np.number]],
    without_baseline_drift_datas: np.ndarray[tuple[int, int, int], np.dtype[np.number]],
    peaks: list[list[tuple[np.ndarray, np.ndarray]]],
    filter_titles: Sequence[str],
    fig_title: str = "",
) -> None:
    cols = filtered_datas.shape[0]
    rows = filtered_datas.shape[1] * 2 + 1
    fig, ax = plt.subplots(rows, cols, figsize=(10 * cols, 4 * rows), sharey=False)
    if fig_title: fig.suptitle(fig_title, fontsize=30)
    axes_matrix = np.atleast_2d(ax)

    for index in range(rows):
        for i in range(cols):
            axes_matrix[index, i].plot(compare_datas[i], color="black", linestyle="--", alpha=0.8, label="ЭКГ")
            axes_matrix[index, i].grid(True, linestyle=":", alpha=0.6)
            axes_matrix[index, i].legend()

    for index, dirty_data in enumerate(filtering_datas):
        axes_matrix[0, index].plot(dirty_data, color="red", alpha=0.6, label="Зашумленный сигнал")
        axes_matrix[0, index].set_title("До фильтрации", fontsize=12)

        for i in range(filtered_datas.shape[1]):
            data = filtered_datas[index][i]
            data_without_drift = without_baseline_drift_datas[index][i]

            axes_matrix[2*i+1, index].plot(data, color="blue", linewidth=2, label="Отфильтрованный сигнал")
            axes_matrix[2*i+1, index].set_title(f"После фильтрации ({filter_titles[i]})", fontsize=12)

            axes_matrix[2*i+2, index].plot(data_without_drift, color="purple", linewidth=2, label="сигнал без дрейфа изолинии")
            axes_matrix[2*i+2, index].set_title(f"После удаления дрейфа изолинии ({filter_titles[i]})", fontsize=12)

    for index in range(len(peaks)):
        for i in range(len(peaks[index])):
            peak_indices, peak_values = peaks[index][i]

            if peak_indices.size > 0:
                axes_matrix[2*i+2, index].scatter(
                    peak_indices,
                    peak_values,
                    color="green",
                    s=40,
                    zorder=5,
                    label="Найденные пики"
                )

            axes_matrix[2*i+2, index].legend()

    fig.tight_layout()
    plt.show()