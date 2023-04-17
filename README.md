# predicates

`predicates` is a module designed to make it easy to create and manipulate complex boolean logic chains. It defines various callable objects (Predicates) that evaluate a boolean based on a provided rule, and it allows you to build up more complex chains of logic by combining Predicates using common set operations (intersection, union, difference, etc.).

## Usage

### Defining Predicates

To create a new Predicate, pass a callable that takes one argument and returns a boolean (truthy or falsy) value to the `Predicate` constructor:

```python
from predicates import Predicate

def is_even(number):
    return number % 2 == 0

even_predicate = Predicate(is_even)
```

You can also use the `@predicate` decorator to convert a function into a Predicate directly:

```python
from predicates import predicate

@predicate
def is_even(number):
    return number % 2 == 0
```

This might seem like overkill for simple logic functions, but the real magic starts when you combine `Predicates`.

### Compound Predicates

Predicates can be combined using common set operations:

- Intersection (`&`): All rules must be true.
- Union (`|`): At least one rule must be true.
- Difference (`-`): One rule must be true, and another rule must be false.
- Exclusive Predicate Union (`^`): Exactly one rule must be true.
- Inversion (`~`): A rule must be false.

For example, to create a Predicate that checks if a number is both even and positive:

```python
@predicate
def is_positive(number):
    return number > 0

@predicate
def is_even(number):
    return number % 2 == 0

even_and_positive = is_even & is_positive

# equivalent to PredicateIntersection(is_even, is_positive)
```
This logic can get very complex, but can still be very expressive.
```python
rule = is_integer & ((is_even & is_positive) | (is_odd & is_multiple_of_3))
```

### Filtering with Predicates

You can filter an iterable based on a Predicate using the `filtered` method:

```python
numbers = range(-10, 11)
even_and_positive_numbers = list(even_and_positive.filtered(numbers))
```

### Predicate Factories

Predicate factories are functions that return a new Predicate based on some input. You can create a Predicate factory using the `predicate_factory` decorator:

```python
from predicates import predicate_factory

@predicate_factory
def divisible_by(divisor):
    def inner(number):
        return number % divisor == 0
    return inner

divisible_by_3 = divisible_by(3)
divisible_by_5 = divisible_by(5)
```

You can then use the generated `Predicates` just like any other `Predicate`:

```python
numbers = range(1, 21)
n_divisible_by_3 = list(divisible_by_3.filtered(numbers))
print(f"Numbers divisible by 3: {n_divisible_by_3}")

divisible_by_3_and_5 = divisible_by(3) & divisible_by(5)
common_multiples = list(divisible_by_3_and_5.filtered(numbers))
print(f"Numbers divisible by both 3 and 5: {common_multiples}")
```

## Aliases

`predicates` provides some type aliases to make the intent of compound `Predicates` extremely clear.

- `Rule`: Alias for `Predicate`.
- `All`: Alias for `PredicateIntersection`.
- `Any`: Alias for `PredicateUnion`.
- `OnlyOne`: Alias for `ExclusivePredicateUnion`.
- `ATrueBFalse`: Alias for `PredicateDifference`.

For example, rather than using `^` or `ExclusivePredicateUnion` to define an "exclusive-or" relationship, you can use the more-expressive `OnlyOne`:

```python
rule = OnlyOne(is_even, is_positive, is_divisible_by_three)
```
