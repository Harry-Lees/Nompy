# Nompy

A Python [parser combinator](https://en.wikipedia.org/wiki/Parser_combinator) library inspired by the [Nom](https://github.com/rust-bakery/nom) library in Rust. This project is in no way affiliated with the original Nom Rust project.

## Examples

### Parse Name

Parse a name and apply a simple transformation.

```python
from nom.combinators import succeeded, tag, take_rest, take_until, tuple_
from nom.modifiers import apply

to_parse = "john doe"

parser = tuple_(
    apply(succeeded(take_until(" "), tag(" ")), str.capitalize),
    apply(take_rest(), str.capitalize),
)
result, remaining = parser(to_parse)
firstname, lastname = result
print(firstname, lastname)  # John Doe
```


### Parse Phone Number

Parse an MSISDN with preceeding `+`

```python
from nom.combinators import preceeded, tag, take_while

to_parse = "+1234567890"

parser = preceeded(take_while(str.isnumeric), tag("+"))
result, remaining = parser(to_parse)
print(result)
```