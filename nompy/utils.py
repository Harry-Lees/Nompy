from typing import Generic, NamedTuple, TypeVar

T = TypeVar("T")


class CombinatorResult(Generic[T], NamedTuple):
    value: T
    remaining: str
