from nompy.combinators import alt, tag
from nompy.modifiers import apply


def test_apply_char_input() -> None:
    parser = apply(tag("A"), ord)
    result, remaining = parser("A")

    assert result == 65
    assert remaining == ""


def test_apply_str_input() -> None:
    parser = apply(tag("hello"), str.upper)
    result, remaining = parser("hello")

    assert result == "HELLO"
    assert remaining == ""
