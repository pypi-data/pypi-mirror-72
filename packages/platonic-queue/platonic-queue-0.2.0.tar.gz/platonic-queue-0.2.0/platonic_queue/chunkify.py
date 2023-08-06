from typing import Iterable, List, TypeVar

T = TypeVar('T')


def chunkify(lst: Iterable[T], chunk_size: int) -> Iterable[List[T]]:
    """Split list into chunks of size not larger than the given number."""
    chunk = []
    for item in lst:  # noqa: WPS110
        chunk.append(item)

        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []

    if chunk:
        yield chunk
