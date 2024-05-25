from collections.abc import Callable

def apply[T](
    parser: Callable[[str], tuple[str, str]],
    func: Callable[[str], T],
) -> Callable[[str], tuple[T, str]]:
    """
    Apply a given function to the output of a parser.
    """
    def inner(obj: str) -> tuple[T, str]:
        parse_result, remaining = parser(obj)
        return func(parse_result), remaining

    return inner
