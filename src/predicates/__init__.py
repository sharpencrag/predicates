import typing as t
from functools import wraps


TruthFinder = t.Callable[[t.Any], bool]


def always_true(_):
    """Placeholder function that always evaluates to True"""
    return True


def always_false(_):
    """Placeholder function that always evaluates to True"""
    return False


class Predicate:
    """Callable object that evaluates a boolean based on a callable rule.

    Predicate objects are a modular way to build complex chains of logic.
    See the Predicate subclasses in this module for more.

    Args:
        rule (callable): A callable that evaluates to a truthy or falsy
            value, given exactly one argument.
    """

    def __init__(self, rule: TruthFinder):
        self.rule = rule

    def item_passes(self, item: t.Any) -> bool:
        """The given item passes the Predicate's rule."""
        return self.rule(item)

    def filtered(self, iterable: t.Iterable) -> t.Iterator:
        """Returns a an iterator of items for which the Predicate is valid

        Args:
            iterable: any iterable of items that are able to be evaluated
                by the Predicate's rule
        """
        return filter(self, iterable)

    def __call__(self, item: t.Any) -> bool:
        return self.item_passes(item)

    def __and__(self, other: TruthFinder) -> "PredicateIntersection":
        return PredicateIntersection(self, other)

    def __or__(self, other: TruthFinder) -> "PredicateUnion":
        return PredicateUnion(self, other)

    def __sub__(self, other: TruthFinder) -> "PredicateDifference":
        return PredicateDifference(self, other)

    def __invert__(self) -> "PredicateDifference":
        return PredicateDifference(always_true, self)

    def __xor__(self, other) -> "ExclusivePredicateUnion":
        return ExclusivePredicateUnion(self, other)


class PredicateIntersection(Predicate):
    """Represents a set of rules which must ALL be True"""

    def __init__(self, *rules: TruthFinder):
        self.rules = rules

    def item_passes(self, item: t.Any) -> bool:
        return all(rule(item) for rule in self.rules)


class PredicateUnion(Predicate):
    """Represents a set of rules where ANY rule must be True"""

    def __init__(self, *rules: TruthFinder):
        self.rules = rules

    def item_passes(self, item):
        return any(rule(item) for rule in self.rules)


class ExclusivePredicateUnion(Predicate):
    """Represents a set of rules where ONLY ONE rule must be True"""

    def __init__(self, *rules: TruthFinder):
        self.rules = rules

    def item_passes(self, item):
        # exploits the fact that booleans are ints
        return sum(rule(item) for rule in self.rules) == 1


class PredicateDifference(Predicate):
    """Represents an A minus B set operation of rules.

    For a given item to pass, a must return True, and b must
    return False
    """

    def __init__(self, a: TruthFinder, b: TruthFinder):
        self.rule_a = a
        self.rule_b = b

    def item_passes(self, item: t.Any) -> bool:
        """The given item passes one rule but fails another.

        Args:
            item (object): any object to check for validity

        Returns: bool
        """
        return self.rule_a(item) and not self.rule_b(item)


def predicate(rule: TruthFinder) -> Predicate:
    """Decorator to convert a function into a Predicate.

    Args:
        rule (callable): a callable that takes exactly one argument
            and returns a truthy or falsy value

    Returns: Predicate
    """
    return Predicate(rule)


def predicate_factory(
    func: t.Callable[[t.Any], TruthFinder]
) -> t.Callable[[t.Any], Predicate]:
    """Decorator to convert a function into a Predicate factory.

    Args:
        func (callable): a callable that returns another truth-finding callable

    Returns: Predicate-producing callable
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return Predicate(func(*args, **kwargs))

    return wrapper


# Aliases

Rule = Predicate
All = PredicateIntersection
Any = PredicateUnion
OnlyOne = ExclusivePredicateUnion
ATrueBFalse = PredicateDifference
