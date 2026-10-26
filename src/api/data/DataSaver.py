from abc import abstractmethod

from src.api.data.DataWorker import DataWorker


class DataSaver[T](DataWorker):
    @abstractmethod
    def save_data(self, data: T) -> None: ...