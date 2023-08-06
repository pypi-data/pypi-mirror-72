from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')


class SerdeStringMixin(ABC, Generic[T]):
    """Serialize and deserialize values."""

    @abstractmethod
    def serialize(self, instance: T) -> str:
        """Convert arbitrary value to a string."""

    @abstractmethod
    def deserialize(self, serialized_string: str) -> T:
        """Convert a serialized value received over the wire to an instance."""
