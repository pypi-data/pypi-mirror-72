from typing import List, TypeVar

from platonic_queue.queue import Queue

T = TypeVar('T')


class LIFOListQueue(Queue[T]):
    """LIFO queue implemented upon a Python list."""

    lst: List[T]

    def __init__(self):
        self.lst = []

    def put(self, instance: T) -> None:
        """Insert element at the tail of the list."""
        self.lst.append(instance)

    def get(self) -> T:
        """Get and remove element from the head of the list."""
        return self.lst.pop()
