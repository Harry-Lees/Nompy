from collections.abc import Callable
from itertools import chain
from typing import TypeAlias

CombinatorResult: TypeAlias = Callable[[str], tuple[str, str]]
Combinator: TypeAlias = Callable[..., CombinatorResult]


def take_until(
    tag: str,
) -> CombinatorResult:
    def inner(obj: str) -> tuple[str, str]:
        _iter = iter(obj)
        matches = []

        while token := next(_iter):
            if token == tag:
                break
            matches.append(token)

        return ("".join(matches), "".join(chain(token, _iter)))

    return inner


def take(n: int = 1) -> CombinatorResult:
    """
    Take `n` elements from the input.
    """

    def inner(obj: str) -> tuple[str, str]:
        _iter = iter(obj)
        return (
            "".join(next(_iter) for _ in range(n)),
            "".join(_iter),
        )

    return inner


def tuple_(
    *args: Combinator,
) -> Callable[[str], tuple[tuple[str, ...], str]]:
    """
    Apply a sequence of parsers consecutively and return a tuple
    of the results.
    """

    def inner(obj: str) -> tuple[tuple[str, ...], str]:
        results = []
        initial_func, *rest = args
        result, remaining = initial_func(obj)
        results.append(result)

        for arg in rest:
            result, remaining = arg(remaining)
            results.append(result)

        return tuple(results), remaining

    return inner


def tag(
    tag: str,
) -> CombinatorResult:
    def inner(obj: str) -> tuple[str, str]:
        _iter = iter(obj)
        result, remaining = take(len(tag))(_iter)

        if result != tag:
            raise ValueError("Tokens do not match given tag")

        return result, remaining

    return inner


def take_rest() -> CombinatorResult:
    """
    Consume the remaining input stream
    """

    def inner(obj: str) -> tuple[str, str]:
        return obj, ""

    return inner


def succeeded(
    first: Combinator,
    second: Combinator,
) -> CombinatorResult:
    """
    Apply two parsers to the given input, and discard the result
    of the second parser.
    """

    def inner(obj: str) -> tuple[str, str]:
        result, remaining = first(obj)
        _, remaining = second(remaining)

        return result, remaining

    return inner


if __name__ == "__main__":
    parser = tuple_(
        succeeded(tag("Hello"), tag(" ")),
        take_rest(),
    )
    result, rest = parser("Hello World")
    print(result)
    print(rest)
