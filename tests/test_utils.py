from nom.utils import CombinatorResult


def test_combinator_result() -> None:
    result = CombinatorResult("Hello", "World")
    assert result.value == "Hello"
    assert result.remaining == "World"
