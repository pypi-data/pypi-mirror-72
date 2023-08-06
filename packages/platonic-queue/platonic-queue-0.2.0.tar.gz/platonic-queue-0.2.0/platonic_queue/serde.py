from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class SerializeToString(ABC, Generic[T]):
    """Serialize value to send through a medium."""

    @abstractmethod
    def serialize(self, instance: T) -> str:
        """Convert arbitrary value to a string."""


class DeserializeFromString(ABC, Generic[T]):
    """Serialize value received via a medium."""

    @abstractmethod
    def deserialize(self, serialized_string: str) -> T:
        """Convert a serialized value received over the wire to an instance."""
