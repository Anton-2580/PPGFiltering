from typing import LiteralString, Any
from pathlib import Path
import numpy as np

from src.api.domain import PeakFinder
from src.impl.data import FileDataReader, FileDataSaver
from src.impl.domain import BaselineDriftRemoverImpl, PeakFinderImpl, PulseBandPowerCalculatorImpl, InsertionSorter, \
    MedianFilter, ExponentialSmoothingFilter, MovingAverageFilter
from src.impl.presentation import filter_visualizer, r_peaks_visualizer


def get_files(hz: float) -> tuple[np.ndarray, ...]:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"

    def load_file(filename: Path | str, res_type: Any, sep: LiteralString = ";", names: bool = False) -> np.ndarray:
        with FileDataReader(str(DATA_DIR / filename), sep=sep, names=names) as file:
            file_data = file.read_data()

        actual_types = [i[1] for i in file_data.dtype.descr]
        if res_type != actual_types:
            raise ValueError(f"Формат файла не совпадает по типам колонок. (dtype {actual_types} != {res_type})")
        return file_data


    types = (
        ['<U4', '<i8', '<i8', '<f8', '<U30'],  # _описание.csv
        ['<f8'],  # fpg
        ['<f8'],  # fpg ЭКГ
        ['<i8', '<f8'],  # ЭТАЛОН_R_зубцы
    )
    return (
        load_file("_описание.csv", types[0], names=True),

        load_file(f"fpg_sit_{hz}Hz.txt", types[1]),
        load_file(f"fpg_sit_ЭКГ_{hz}Hz.txt", types[2]),
        load_file("fpg_sit_ЭТАЛОН_R_зубцы.csv", types[3], sep=",", names=True),

        load_file(f"fpg_walk_{hz}Hz.txt", types[1]),
        load_file(f"fpg_walk_ЭКГ_{hz}Hz.txt", types[2]),
        load_file("fpg_walk_ЭТАЛОН_R_зубцы.csv", types[3], sep=",", names=True),
    )


def save_file(filename: str, data: np.ndarray[tuple[int]], fmt: str = "%s", sep: LiteralString = ";") -> None:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "res_data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with FileDataSaver(DATA_DIR / filename, sep=sep, fmt=fmt) as file:
        file.save_data(data)


def get_r_peaks(data: tuple[np.ndarray, ...]) -> list[np.ndarray]:
    r_peaks = []
    for i in data[3::3]:
        if (names := i.dtype.names) is None:
            raise ValueError("Ожидался структурированный массив с именами колонок.")

        field_name = names[1]
        r_peaks.append(i[field_name])
    return r_peaks


def calc_peaks(
    hz: float,
    without_baseline_drift_datas: np.ndarray,
    peak_finder: PeakFinder
) -> tuple[
        np.ndarray[tuple[int, int], np.dtype[np.integer]],
        np.ndarray[tuple[int, int], np.dtype[np.floating]],
        np.ndarray[tuple[int, int], np.dtype[np.floating]],
        list[list[tuple[np.ndarray, np.ndarray]]],
]:
    res_peaks: list[list[tuple[np.ndarray, np.ndarray]]] = []
    count_peaks = np.zeros(without_baseline_drift_datas.shape[:2], dtype=np.int64)
    mean_intervals = np.zeros(without_baseline_drift_datas.shape[:2], dtype=np.float64)
    spread_mean_intervals = np.zeros(without_baseline_drift_datas.shape[:2], dtype=np.float64)

    for index, item in enumerate(without_baseline_drift_datas):
        res_peaks.append([])
        for i, j in enumerate(item):
            indexes = peak_finder.search_with_std(j)
            res_peaks[-1].append((indexes, j[indexes]))

            peak = indexes / hz * 1000
            count_peaks[index, i] = peak.shape[0]
            interval = np.diff(peak)

            mean_intervals[index, i] = np.mean(interval)
            spread_mean_intervals[index, i] = np.std(interval)

    return count_peaks, mean_intervals, spread_mean_intervals, res_peaks


def calc_reference_peaks(
    r_peaks: list[np.ndarray],
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    modes_count = len(r_peaks)

    count_peaks = np.zeros(modes_count, dtype=np.int64)
    mean_intervals = np.zeros(modes_count, dtype=np.float64)
    spread_mean_intervals = np.zeros(modes_count, dtype=np.float64)

    for index, peak_indexes in enumerate(r_peaks):
        peak_time_ms = peak_indexes * 1000
        count_peaks[index] = peak_time_ms.shape[0]

        interval = np.diff(peak_time_ms)
        mean_intervals[index] = np.mean(interval)
        spread_mean_intervals[index] = np.std(interval)

    return count_peaks, mean_intervals, spread_mean_intervals


def main() -> None:
    try:
        Hz = 125
        data = get_files(Hz)
        r_peaks = get_r_peaks(data)

        N, alpha = int(input("N: ")), float(input("alpha: "))
        medianFilter = MedianFilter(N, InsertionSorter)
        movingAverageFilter = MovingAverageFilter(N)
        exponentialSmoothingFilter = ExponentialSmoothingFilter(alpha)

        medianFilter.check_window_size(data[0][0][1])
        medianFilter.check_window_size(data[0][1][1])
    except Exception as e:
        print(e)
        return

    baselineDriftRemover = BaselineDriftRemoverImpl(time=2, Hz=Hz, filter=MovingAverageFilter)
    peakFinderImpl = PeakFinderImpl(refractory_period=0.3, Hz=Hz)
    pulseBandPowerCalculator = PulseBandPowerCalculatorImpl(Hz=Hz)

    compare_datas = data[2], data[5]
    filtering_datas = data[1], data[4]
    filters = (medianFilter, movingAverageFilter, exponentialSmoothingFilter)
    filter_titles = ("медианный", "скольз.сред.", "эксп.сглаж.")

    filtered_datas = np.array([
        [j.filter(i) for j in filters]
        for i in filtering_datas
    ])
    without_baseline_drift_datas = np.array([
        [baselineDriftRemover.remove_baseline_drift(j) for j in i]
        for i in filtered_datas
    ])
    power_ratios = [
        [pulseBandPowerCalculator.calc(j) for j in i]
        for i in filtered_datas
    ]
    count_peaks, mean_intervals, spread_mean_intervals, peaks = calc_peaks(Hz, without_baseline_drift_datas, peakFinderImpl)

    modes = "sit", "walk"
    for i, mode in enumerate(modes):
        for index, title in enumerate(filter_titles):
            save_file(rf"{mode}_{title}.csv", filtered_datas[i][index])

    save_file(
        "info.csv",
        np.array([("Режим", "Фильтр", "Число волн", "Средний интервал (мс)", "Разброс СКО (мс)", "Доля мощности")] + [
            (mode, title, count_peaks[i, index], mean_intervals[i, index], spread_mean_intervals[i, index], power_ratios[i][index])
            for i, mode in enumerate(modes)
                for index, title in enumerate(filter_titles)
        ])
    )

    count_ref, mean_ref, spread_ref = calc_reference_peaks(r_peaks)
    save_file(
        "reference_info.csv",
        np.array([("Режим", "число сокращений сердца", "средний интервал между ними (мс)", "разброс СКО (мс)")] + [
            (mode, count_ref[i], mean_ref[i], spread_ref[i])
            for i, mode in enumerate(modes)
        ])
    )

    filter_visualizer(
        compare_datas=compare_datas,
        filtering_datas=filtering_datas,
        filtered_datas=filtered_datas,
        without_baseline_drift_datas=without_baseline_drift_datas,
        peaks=peaks,
        filter_titles=filter_titles,
        fig_title=f"N: {N}, alpha: {alpha}",
    )

    r_peaks_visualizer(
        r_peaks,
        ("fpg_sit_ЭТАЛОН_R_зубцы", "fpg_walk_ЭТАЛОН_R_зубцы"),
    )


if __name__ == "__main__":
    main()