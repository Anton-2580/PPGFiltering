import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np

from main import main, get_files
from src.impl.domain import MedianFilter, MovingAverageFilter, InsertionSorter


class ExperimentWithoutFiltering(unittest.TestCase):

    @patch("builtins.input", side_effect=["21", "0.5"])
    @patch("main.MedianFilter.filter")
    @patch("main.MovingAverageFilter.filter")
    @patch("main.ExponentialSmoothingFilter.filter")
    @patch("main.r_peaks_visualizer")
    def test_experiment_without_filtering(
        self,
        mock_vis2: MagicMock,
        mock_expo_filter: MagicMock,
        mock_ma_filter: MagicMock,
        mock_median_filter: MagicMock,
        mock_input: MagicMock,
    ) -> None:
        mock_vis2.side_effect = lambda *args, **kwargs: None
        identity_filter = lambda data: data

        mock_expo_filter.side_effect = identity_filter
        mock_ma_filter.side_effect = identity_filter
        mock_median_filter.side_effect = identity_filter

        main()

        path = Path(__file__).parent / "res_data" / "info.csv"
        res_data = np.genfromtxt(path, delimiter=';', names=True, dtype=None, encoding="utf-8")

        print(res_data)

    @patch("builtins.input")
    @patch("main.MedianFilter.filter")
    @patch("main.ExponentialSmoothingFilter.filter")
    @patch("main.filter_visualizer")
    @patch("main.r_peaks_visualizer")
    def test_experiment_best_window_size_for_ma(
        self,
        mock_vis1: MagicMock,
        mock_vis2: MagicMock,
        mock_expo_filter: MagicMock,
        mock_median_filter: MagicMock,
        mock_input: MagicMock,
    ) -> None:
        identity_filter = lambda data: data

        mock_expo_filter.side_effect = identity_filter
        mock_median_filter.side_effect = identity_filter

        mock_vis1.side_effect = lambda *args, **kwargs: None
        mock_vis2.side_effect = lambda *args, **kwargs: None

        N = 3, 5, 9, 15, 25, 41, 61
        results = []

        for n in N:
            mock_input.side_effect = [str(n), "0.5"]

            main()

            path = Path(__file__).parent / "res_data" / "info.csv"
            res_data = np.genfromtxt(path, delimiter=';', names=True, dtype=None, encoding="utf-8")
            print(res_data[1::3], "\t\t", n)
            results.append((res_data[1][5] + res_data[4][5], n))

        best = max(results)
        print("Лучший результат MovingAverageFilter при окне:", best[1])

    @patch("builtins.input")
    # @patch("main.filter_visualizer")
    @patch("main.r_peaks_visualizer")
    def test_compare_filters(
        self,
        mock_vis1: MagicMock,
        # mock_vis2: MagicMock,
        mock_input: MagicMock,
    ) -> None:
        mock_vis1.side_effect = lambda *args, **kwargs: None
        # mock_vis2.side_effect = lambda *args, **kwargs: None
        path = Path(__file__).parent / "res_data" / "info.csv"

        alpha = 0.05, 0.1, 0.2, 0.4, 0.8
        N = 9, 15, 25, 41, 61

        i = 0
        res = []
        for a, n in zip(alpha, N):
            mock_input.side_effect = [str(n), str(a)]

            main()

            res_data = np.genfromtxt(path, delimiter=';', names=True, dtype=None, encoding="utf-8")
            if (file_names := res_data.dtype.names) is None:
                self.assertTrue(False)
                return

            combined = np.zeros(res_data.shape, dtype=np.dtype([('Параметр', '<f8')] + res_data.dtype.descr))
            for field in file_names:
                combined[field] = res_data[field]
            combined["Параметр"] = n
            combined["Параметр"][2::3] = a

            res.append(combined)
            i += 1

        result = np.concatenate(res)
        np.savetxt(
            path.parent / "exp.csv",
            result,
            fmt="%s",
            header=";".join(result.dtype.names or ()),
            delimiter=";",
            comments="",
            encoding="utf-8"
        )

    def test_creating_noise(self) -> None:
        impulse_data, uniform_data, clean_data = self.corrupt_data()
        N = 3, 5, 9, 15, 25

        medianFilter = MedianFilter(N[0], InsertionSorter)
        movingAverageFilter = MovingAverageFilter(N[0])

        errors = {}
        for n in N:
            medianFilter.N = n
            movingAverageFilter.N = n

            data = {
                "movingAverage_impulse_data": movingAverageFilter.filter(impulse_data),
                "median_impulse_data": medianFilter.filter(impulse_data),
                "movingAverage_uniform_data": movingAverageFilter.filter(uniform_data),
                "median_uniform_data": medianFilter.filter(uniform_data),
            }

            errors[n] = {k: float(np.sqrt(np.mean((v - clean_data) ** 2))) for k, v in data.items()}

        # pprint(errors)
        print("", "Помеха", "Фильтр", "   Окно", "Ошибка (RMSE)", sep="\t\t", end="\n\n")
        for n in N:
            for error in errors[n]:
                mode = "Импульсная" if "impulse" in error else "Равномерная"
                filter_name = "Медианный         " if "median" in error else "Скользящее среднее"

                print("", mode, filter_name, n, errors[n][error], "", sep="\t")


    @staticmethod
    def corrupt_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        np.random.seed(0)

        clean_data = get_files(125)[1]
        impulse_data = clean_data.copy()
        uniform_data = clean_data.copy()

        plus_minus = np.ones(clean_data.shape[0] // 100, dtype=np.int8)
        plus_minus[1::2] = -1
        impulse_data[99::100] = plus_minus * 8

        uniform_data += np.random.uniform(low=-0.9, high=0.9, size=impulse_data.shape[0])

        return impulse_data, uniform_data, clean_data


if __name__ == "__main__":
    unittest.main()