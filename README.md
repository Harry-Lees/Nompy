# Nompy

A Python [parser combinator](https://en.wikipedia.org/wiki/Parser_combinator) library similar to Nom for Rust.

## Examples

Parse a name and apply a simple transformation.

```python
from nompy.combinators import succeeded, tag, take_rest, take_until, tuple_
from nompy.modifiers import apply

to_parse = "john doe"

parser = tuple_(
    apply(succeeded(take_until(" "), tag(" ")), str.capitalize),
    apply(take_rest(), str.capitalize),
)
result, remaining = parser(to_parse)
firstname, lastname = result
print(firstname, lastname)
```
