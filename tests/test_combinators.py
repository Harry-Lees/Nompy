from nompy.combinators import alt, preceeded, succeeded, tag, take_while


def test_alt_first() -> None:
    parser = alt(
        tag("Hello"),
        tag("World"),
    )
    result, remaining = parser("Hello")
    assert result == "Hello"
    assert remaining == ""


def test_alt_second() -> None:
    parser = alt(
        tag("Hello"),
        tag("World"),
    )
    result, remaining = parser("World")
    assert result == "World"
    assert remaining == ""


def test_take_while_remaining_input() -> None:
    parser = take_while(str.isalpha)
    result, remaining = parser("Hello World")
    assert result == "Hello"
    assert remaining == " World"


def test_take_while_consumes_full_input() -> None:
    parser = take_while(str.isdecimal)
    result, remaining = parser("0123456789")
    assert result == "0123456789"
    assert remaining == ""
