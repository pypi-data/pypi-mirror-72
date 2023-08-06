from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar('T')  # noqa: WPS111


class BaseQueue(ABC, Generic[T]):
    """Base class for queues."""


class InputQueue(BaseQueue[T]):
    """Queue to read stuff from."""

    @abstractmethod
    def get(self) -> T:
        """Get next instance from queue."""


class OutputQueue(BaseQueue[T]):
    """Queue to write stuff into."""

    @abstractmethod
    def put(self, instance: T) -> None:
        """Put a message into the queue."""

    def put_many(self, iterable: Iterable[T]) -> None:
        """Put multiple messages into the queue."""
        for instance in iterable:
            self.put(instance)


class InputOutputQueue(InputQueue[T], OutputQueue[T]):
    """Queue to write to and to read from."""
