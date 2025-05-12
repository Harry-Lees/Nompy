from typing import Generic, TypeVar

from typing_extensions import NamedTuple

T = TypeVar("T")


class CombinatorResult(Generic[T], NamedTuple):
    value: T
    remaining: str
