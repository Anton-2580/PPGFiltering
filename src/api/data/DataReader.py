from abc import abstractmethod

from src.api.data.DataWorker import DataWorker


class DataReader[T](DataWorker):
    @abstractmethod
    def read_data(self) -> T: ...