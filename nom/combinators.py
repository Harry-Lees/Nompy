from collections.abc import Callable
from itertools import chain
from typing import Any, TypeVar

from nom.utils import CombinatorResult

T = TypeVar("T")


def take_while(
    pred: Callable[[str], bool],
):
    """
    Take elements from the input while the given predicate
    function evaluates to True.
    """

    def inner(obj: str) -> CombinatorResult[str]:
        _iter = iter(obj)
        consumed = []
        try:
            while token := next(_iter):
                if pred(token) is False:
                    break

                consumed.append(token)
        except StopIteration:
            return CombinatorResult(
                "".join(consumed),
                "",
            )
        else:
            return CombinatorResult(
                "".join(consumed),
                "".join(chain(token, _iter)),
            )

    return inner


def take_until(
    pred: Callable[[str], bool],
):
    """
    Take elements from the input until the given predicate
    returns True.
    """

    return take_while(lambda x: not pred(x))


def take(n: int = 1) -> Callable[[str], CombinatorResult[str]]:
    """
    Take `n` elements from the input.
    """

    if n < 0:
        raise ValueError("n must be greater than 0")

    def inner(obj: str) -> CombinatorResult[str]:
        if len(obj) < n:
            raise ValueError("Not enough elements in input")

        _iter = iter(obj)
        return CombinatorResult(
            "".join(next(_iter) for _ in range(n)),
            "".join(_iter),
        )

    return inner


def alt(
    *args: Callable[..., CombinatorResult[Any]],
) -> Callable[[str], CombinatorResult[Any]]:
    """
    Try a sequence of parsers, return the result of the
    first successful one.
    """

    def inner(obj: str) -> CombinatorResult[Any]:
        for arg in args:
            try:
                return arg(obj)
            except ValueError:
                pass

        raise ValueError("No parsers succeeded")

    return inner


def tuple_(
    *args: Callable[..., CombinatorResult[Any]],
) -> Callable[[str], CombinatorResult[tuple[str, ...]]]:
    """
    Apply a sequence of parsers consecutively and return a tuple
    of the results.
    """

    if len(args) < 1:
        raise ValueError("At least one parser is required")

    def inner(obj: str) -> CombinatorResult[tuple[str, ...]]:
        results = []
        initial_func, *rest = args
        result, remaining = initial_func(obj)
        results.append(result)

        for arg in rest:
            result, remaining = arg(remaining)
            results.append(result)

        return CombinatorResult(tuple(results), remaining)

    return inner


def tag(
    tag: str,
) -> Callable[[str], CombinatorResult[str]]:
    def inner(obj: str) -> CombinatorResult[str]:
        result, remaining = take(len(tag))(obj)

        if result != tag:
            raise ValueError("Tokens do not match given tag")

        return CombinatorResult(result, remaining)

    return inner


def tag_no_case(tag: str) -> Callable[[str], CombinatorResult[str]]:
    def inner(obj: str) -> CombinatorResult[str]:
        result, remaining = take(len(tag))(obj)

        if result.lower() != tag.lower():
            raise ValueError("Tokens do not match given tag")

        return CombinatorResult(result, remaining)

    return inner


def take_rest() -> Callable[[str], CombinatorResult[str]]:
    """
    Consume the remaining input stream
    """

    def inner(obj: str) -> CombinatorResult[str]:
        return CombinatorResult(obj, "")

    return inner


def succeeded(
    first: Callable[[str], CombinatorResult[T]],
    second: Callable[[str], CombinatorResult[Any]],
) -> Callable[[str], CombinatorResult[T]]:
    """
    Apply two parsers to the given input, and discard the result
    of the second parser.
    """

    def inner(obj: str) -> CombinatorResult[T]:
        result, remaining = first(obj)
        _, remaining = second(remaining)

        return CombinatorResult(result, remaining)

    return inner


def preceeded(
    parser: Callable[[str], CombinatorResult[T]],
    preceeded_by: Callable[[str], CombinatorResult[Any]],
) -> Callable[[str], CombinatorResult[T]]:
    """
    Applies two parsers to the input, ensures that the first parser is
    preceeded by the second parser. Discards the results of the second parser.
    """

    def inner(obj: str) -> CombinatorResult[T]:
        _, remaining = preceeded_by(obj)
        result, remaining = parser(remaining)

        return CombinatorResult(result, remaining)

    return inner


def opt(
    parser: Callable[[str], CombinatorResult[T]],
) -> Callable[[str], CombinatorResult[T] | CombinatorResult[None]]:
    """
    Makes the given parser optional.
    """

    def inner(obj: str) -> CombinatorResult[T] | CombinatorResult[None]:
        try:
            return parser(obj)
        except ValueError:
            return CombinatorResult(None, obj)

    return inner


def recognize(
    parser: Callable[[str], CombinatorResult[Any]],
) -> Callable[[str], CombinatorResult[str]]:
    """
    Parse an input stream and return the parsed values
    """

    def inner(obj: str) -> CombinatorResult[str]:
        before = obj
        _, remaining = parser(obj)
        processed = before.removesuffix(remaining)

        return CombinatorResult(processed, remaining)

    return inner


def count(
    parser: Callable[[str], CombinatorResult[T]],
    count: int,
) -> Callable[[str], CombinatorResult[tuple[T, ...]]]:
    """
    Applies the embedded parser `count` number of times, gathering
    the results in a tuple.
    """

    def inner(obj: str) -> CombinatorResult[tuple[T, ...]]:
        results = []
        for _ in range(count):
            result, obj = parser(obj)
            results.append(result)

        return CombinatorResult(tuple(results), obj)

    return inner


def none_of(chars: str) -> Callable[[str], CombinatorResult[str]]:
    """
    Recognizes a character that is not in the provided characters.
    Returns an error if there's not enough input data.
    """

    def inner(obj: str) -> CombinatorResult[str]:
        if len(obj) < 1:
            raise ValueError("Not enough elements in input")

        split_chars = set(chars)
        parsed = obj[0] if obj[0] not in split_chars else None

        if parsed is None:
            raise ValueError("Character could not be recognized in provided charset")

        return CombinatorResult(parsed, obj[1:])

    return inner
