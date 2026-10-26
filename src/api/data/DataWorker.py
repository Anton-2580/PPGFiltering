from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self, Literal


class DataWorker(ABC):
    def __enter__(self) -> Self:
        self._open_resource()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[False]:
        self._close_resource()
        return False

    @abstractmethod
    def _open_resource(self) -> None: ...
    @abstractmethod
    def _close_resource(self) -> None: ...