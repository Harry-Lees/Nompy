from collections.abc import Callable
from typing import TypeVar

RT = TypeVar("RT")


def apply(
    parser: Callable[[str], tuple[str, str]],
    func: Callable[[str], RT],
) -> Callable[[str], tuple[RT, str]]:
    """
    Apply a given function to the output of a parser.
    """

    def inner(obj: str) -> tuple[RT, str]:
        parse_result, remaining = parser(obj)
        return func(parse_result), remaining

    return inner
