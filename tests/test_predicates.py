import pytest
import predicates


def test_always_true():
    assert predicates.always_true(0)
    assert predicates.always_true(None)
    assert predicates.always_true("")
    assert predicates.always_true(42)


def test_always_false():
    assert not predicates.always_false(0)
    assert not predicates.always_false(None)
    assert not predicates.always_false("")
    assert not predicates.always_false(42)


def test_predicate():
    is_even = lambda x: x % 2 == 0
    assert_predicate(predicates.Predicate(is_even))
    assert_predicate(predicates.Rule(is_even))


def assert_predicate(is_even):
    assert is_even(2)
    assert not is_even(3)


def test_predicate_intersection():
    is_even = predicates.Predicate(lambda x: x % 2 == 0)
    is_positive = predicates.Predicate(lambda x: x > 0)
    assert_predicate_intersection(
        predicates.PredicateIntersection(is_even, is_positive)
    )
    assert_predicate_intersection(is_even & is_positive)
    assert_predicate_intersection(predicates.All(is_even, is_positive))


def assert_predicate_intersection(is_even_and_positive):
    assert not is_even_and_positive(-2)
    assert not is_even_and_positive(1)
    assert is_even_and_positive(2)


def test_predicate_union():
    is_even = predicates.Predicate(lambda x: x % 2 == 0)
    is_negative = predicates.Predicate(lambda x: x < 0)
    assert_predicate_union(predicates.PredicateUnion(is_even, is_negative))
    assert_predicate_union(is_even | is_negative)
    assert_predicate_union(predicates.Any(is_even, is_negative))


def assert_predicate_union(is_even_or_negative):
    assert is_even_or_negative(-1)
    assert is_even_or_negative(2)
    assert not is_even_or_negative(3)


def test_exclusive_predicate_union():
    is_positive = predicates.Predicate(lambda x: x > 0)
    is_multiple_of_3 = predicates.Predicate(lambda x: x % 3 == 0)
    assert_exclusive_predicate_union(
        predicates.ExclusivePredicateUnion(is_positive, is_multiple_of_3)
    )
    assert_exclusive_predicate_union(is_positive ^ is_multiple_of_3)
    assert_exclusive_predicate_union(predicates.OnlyOne(is_positive, is_multiple_of_3))


def assert_exclusive_predicate_union(is_positive_xor_multiple_of_3):
    assert is_positive_xor_multiple_of_3(-3)  # not positive and is multiple of 3
    assert not is_positive_xor_multiple_of_3(-2)  # not positive and not multiple of 3
    assert is_positive_xor_multiple_of_3(2)  # positive and not multiple of 3
    assert not is_positive_xor_multiple_of_3(3)  # positive and multiple of 3


def test_predicate_difference():
    is_even = predicates.Predicate(lambda x: x % 2 == 0)
    is_positive = predicates.Predicate(lambda x: x > 0)
    assert_predicate_difference(predicates.PredicateDifference(is_even, is_positive))
    assert_predicate_difference(is_even - is_positive)
    assert_predicate_difference(predicates.ATrueBFalse(a=is_even, b=is_positive))


def assert_predicate_difference(is_even_and_not_positive):
    assert is_even_and_not_positive(-2)
    assert not is_even_and_not_positive(1)
    assert not is_even_and_not_positive(2)


def test_predicate_decorator():
    @predicates.predicate
    def is_even(x):
        return x % 2 == 0

    assert isinstance(is_even, predicates.Predicate)
    assert is_even(2)
    assert not is_even(3)


def test_predicate_factory_decorator():
    @predicates.predicate_factory
    def threshold(thresh):
        def rule(x):
            return x >= thresh

        return rule

    greater_than_5 = threshold(5)
    assert isinstance(greater_than_5, predicates.Predicate)
    assert greater_than_5(6)
    assert not greater_than_5(4)


def test_predicate_invert_magic_method():
    is_even = predicates.Predicate(lambda x: x % 2 == 0)

    is_not_even = ~is_even
    assert isinstance(is_not_even, predicates.PredicateDifference)
    assert is_not_even(1)
    assert not is_not_even(2)


if __name__ == "__main__":
    pytest.main([__file__])
