from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar('T')  # noqa: WPS111


class Queue(ABC, Generic[T]):
    """Acknowledgement Queue."""

    @abstractmethod
    def put(self, instance: T) -> None:
        """Put a message into the queue."""

    def put_many(self, iterable: Iterable[T]) -> None:
        """Put multiple messages into the queue."""
        for instance in iterable:
            self.put(instance)

    @abstractmethod
    def get(self) -> T:
        """Get next instance from queue."""
