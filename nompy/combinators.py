from collections.abc import Callable
from itertools import chain
from typing import Any, TypeAlias, TypeVar

T = TypeVar("T")

CombinatorResult: TypeAlias = Callable[[str], tuple[T, str]]
Combinator: TypeAlias = Callable[..., CombinatorResult[T]]


def take_while(
    pred: Callable[[str], bool],
) -> CombinatorResult:
    """
    Take elements from the input while the given predicate
    function evaluates to True.
    """

    def inner(obj: str) -> tuple[str, str]:
        _iter = iter(obj)
        consumed = []
        try:
            while token := next(_iter):
                if pred(token) is False:
                    break

                consumed.append(token)
        except StopIteration:
            return (
                "".join(consumed),
                "",
            )
        else:
            return (
                "".join(consumed),
                "".join(chain(token, _iter)),
            )

    return inner


def take_until(
    pred: Callable[[str], bool],
) -> CombinatorResult:
    """
    Take elements from the input until the given predicate
    returns True.
    """

    return take_while(lambda x: not pred(x))


def take(n: int = 1) -> CombinatorResult:
    """
    Take `n` elements from the input.
    """

    if n < 0:
        raise ValueError("n must be greater than 0")

    def inner(obj: str) -> tuple[str, str]:
        if len(obj) < n:
            raise ValueError("Not enough elements in input")

        _iter = iter(obj)
        return (
            "".join(next(_iter) for _ in range(n)),
            "".join(_iter),
        )

    return inner


def alt(
    *args: Combinator,
) -> Callable[[str], tuple[str, str]]:
    """
    Try a sequence of parsers, return the result of the
    first successful one.
    """

    def inner(obj: str) -> tuple[str, str]:
        for arg in args:
            try:
                return arg(obj)
            except ValueError:
                pass

        raise ValueError("No parsers succeeded")

    return inner


def tuple_(
    *args: Combinator,
) -> Callable[[str], tuple[tuple[str, ...], str]]:
    """
    Apply a sequence of parsers consecutively and return a tuple
    of the results.
    """

    if len(args) < 1:
        raise ValueError("At least one parser is required")

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
        result, remaining = take(len(tag))(obj)

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


def preceeded(
    parser: Combinator[T],
    preceeded_by: Combinator[Any],
) -> CombinatorResult[T]:
    """
    Applies two parsers to the input, ensures that the first parser is
    preceeded by the second parser. Discards the results of the second parser.
    """

    def inner(obj: str) -> tuple[T, str]:
        _, remaining = preceeded_by(obj)
        result, remaining = parser(remaining)

        return result, remaining

    return inner


def opt(
    parser: Combinator[T],
) -> CombinatorResult[T] | CombinatorResult[None]:
    """
    Makes the given parser optional.
    """

    def inner(obj: str):
        try:
            return parser(obj)
        except ValueError:
            return None, obj

    return inner
