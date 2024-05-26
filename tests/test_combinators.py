import pytest

from nompy.combinators import (
    alt,
    opt,
    preceeded,
    succeeded,
    tag,
    take,
    take_rest,
    take_until,
    take_while,
    tuple_,
)


def test_take_rest() -> None:
    parser = take_rest()
    result, remaining = parser("Hello World")
    assert result == "Hello World"
    assert remaining == ""


def test_preceeded_match() -> None:
    parser = preceeded(tag("World"), tag("Hello"))
    result, remaining = parser("HelloWorld")
    assert result == "World"
    assert remaining == ""


def test_preceeded_no_match() -> None:
    parser = preceeded(tag("World"), tag("Hello"))
    with pytest.raises(ValueError):
        parser("Goodbye")


def test_succeeded_match() -> None:
    parser = succeeded(tag("Hello"), tag("World"))
    result, remaining = parser("HelloWorld")
    assert result == "Hello"
    assert remaining == ""


def test_succeeded_no_match() -> None:
    parser = succeeded(tag("Hello"), tag("World"))
    with pytest.raises(ValueError):
        parser("Goodbye")


def test_tag_success() -> None:
    parser = tag("Hello")
    result, remaining = parser("Hello")
    assert result == "Hello"
    assert remaining == ""


def test_tag_failure() -> None:
    parser = tag("Hello")
    with pytest.raises(ValueError):
        parser("World")


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


def test_alt_no_match() -> None:
    parser = alt(
        tag("Hello"),
        tag("World"),
    )
    with pytest.raises(ValueError):
        parser("Goodbye")


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


def test_take_until_match() -> None:
    parser = take_until(str.isspace)
    result, remaining = parser("Hello World")
    assert result == "Hello"
    assert remaining == " World"


def test_take_until_consumes_full_input() -> None:
    parser = take_until(str.isspace)
    result, remaining = parser("HelloWorld")
    assert result == "HelloWorld"
    assert remaining == ""


def test_tuple_multi() -> None:
    parser = tuple_(tag("Hello"), tag("World"))
    result, remaining = parser("HelloWorld")
    assert result == ("Hello", "World")
    assert remaining == ""


def test_tuple_single() -> None:
    parser = tuple_(tag("Hello"))
    result, remaining = parser("HelloWorld")
    assert result == ("Hello",)
    assert remaining == "World"


def test_tuple_fails() -> None:
    parser = tuple_(tag("Hello"), tag("World"))
    with pytest.raises(ValueError):
        parser("Goodbye")


def test_empty_tuple_raises() -> None:
    with pytest.raises(ValueError):
        tuple_()


def test_take_success() -> None:
    parser = take(5)
    result, remaining = parser("Hello")
    assert result == "Hello"
    assert remaining == ""


def test_take_exceeds_input_length() -> None:
    parser = take(10)
    with pytest.raises(ValueError):
        parser("Hello")


def test_take_with_remaining() -> None:
    parser = take(5)
    result, remaining = parser("Hello World")
    assert result == "Hello"
    assert remaining == " World"


def test_take_zero() -> None:
    parser = take(0)
    result, remaining = parser("Hello World")
    assert result == ""
    assert remaining == "Hello World"


def test_take_negative() -> None:
    with pytest.raises(ValueError):
        take(-1)


def test_opt_no_input() -> None:
    parser = opt(tag("+"))
    result, remaining = parser("")
    assert result is None
    assert remaining == ""


def test_opt_with_input() -> None:
    parser = opt(tag("+"))
    result, remaining = parser("+")
    assert result == "+"
    assert remaining == ""
