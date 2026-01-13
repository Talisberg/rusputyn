#!/usr/bin/env python3
"""
Tests for more-itertools-rs

Validates API compatibility with more-itertools package.
"""

import pytest

try:
    import more_itertools_rs as mit
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    pytest.skip("more_itertools_rs not available", allow_module_level=True)


class TestChunked:
    def test_basic(self):
        result = mit.chunked([1, 2, 3, 4, 5, 6], 2)
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_incomplete_chunk(self):
        result = mit.chunked([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_single_element(self):
        result = mit.chunked([1], 3)
        assert result == [[1]]

    def test_strict_mode(self):
        with pytest.raises(ValueError):
            mit.chunked([1, 2, 3], 2, strict=True)

    def test_zero_size(self):
        with pytest.raises(ValueError):
            mit.chunked([1, 2, 3], 0)


class TestBatched:
    def test_basic(self):
        result = mit.batched([1, 2, 3, 4, 5, 6], 2)
        assert result == [(1, 2), (3, 4), (5, 6)]

    def test_incomplete_batch(self):
        result = mit.batched('ABCDEFG', 3)
        assert result == [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]

    def test_strict_mode(self):
        with pytest.raises(ValueError):
            mit.batched([1, 2, 3, 4, 5], 2, strict=True)


class TestFlatten:
    def test_basic(self):
        result = mit.flatten([[1, 2], [3, 4], [5]])
        assert result == [1, 2, 3, 4, 5]

    def test_empty_inner(self):
        result = mit.flatten([[1, 2], [], [3]])
        assert result == [1, 2, 3]

    def test_empty(self):
        result = mit.flatten([])
        assert result == []


class TestFirst:
    def test_basic(self):
        assert mit.first([1, 2, 3]) == 1

    def test_with_default(self):
        assert mit.first([], default=42) == 42

    def test_empty_no_default(self):
        with pytest.raises(ValueError):
            mit.first([])


class TestLast:
    def test_basic(self):
        assert mit.last([1, 2, 3]) == 3

    def test_with_default(self):
        assert mit.last([], default=42) == 42

    def test_empty_no_default(self):
        with pytest.raises(ValueError):
            mit.last([])


class TestTake:
    def test_basic(self):
        result = mit.take(3, [1, 2, 3, 4, 5])
        assert result == [1, 2, 3]

    def test_take_all(self):
        result = mit.take(10, [1, 2, 3])
        assert result == [1, 2, 3]

    def test_take_zero(self):
        result = mit.take(0, [1, 2, 3])
        assert result == []


class TestUniqueEverseen:
    def test_basic(self):
        result = mit.unique_everseen([1, 2, 3, 2, 1, 4])
        assert result == [1, 2, 3, 4]

    def test_preserves_order(self):
        result = mit.unique_everseen([3, 1, 2, 1, 3])
        assert result == [3, 1, 2]

    def test_empty(self):
        result = mit.unique_everseen([])
        assert result == []


class TestPartition:
    def test_basic(self):
        def is_even(x):
            return x % 2 == 0

        false_items, true_items = mit.partition(is_even, [1, 2, 3, 4, 5, 6])
        assert false_items == [1, 3, 5]
        assert true_items == [2, 4, 6]

    def test_all_false(self):
        def is_even(x):
            return x % 2 == 0

        false_items, true_items = mit.partition(is_even, [1, 3, 5])
        assert false_items == [1, 3, 5]
        assert true_items == []


class TestWindowed:
    def test_basic(self):
        result = mit.windowed([1, 2, 3, 4], 2)
        assert result == [(1, 2), (2, 3), (3, 4)]

    def test_size_three(self):
        result = mit.windowed([1, 2, 3, 4, 5], 3)
        assert result == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    def test_with_step(self):
        result = mit.windowed([1, 2, 3, 4, 5, 6], 2, step=2)
        assert result == [(1, 2), (3, 4), (5, 6)]

    def test_empty(self):
        result = mit.windowed([], 2)
        assert result == []


class TestAllUnique:
    def test_all_unique(self):
        assert mit.all_unique([1, 2, 3, 4]) is True

    def test_has_duplicate(self):
        assert mit.all_unique([1, 2, 3, 2]) is False

    def test_empty(self):
        assert mit.all_unique([]) is True


class TestInterleave:
    def test_basic(self):
        result = mit.interleave([1, 2, 3], ['a', 'b', 'c'])
        assert result == [1, 'a', 2, 'b', 3, 'c']

    def test_uneven_lengths(self):
        result = mit.interleave([1, 2], ['a', 'b', 'c', 'd'])
        assert result == [1, 'a', 2, 'b', 'c', 'd']

    def test_three_iterables(self):
        result = mit.interleave([1, 2], ['a', 'b'], ['x', 'y'])
        assert result == [1, 'a', 'x', 2, 'b', 'y']


class TestIsSorted:
    def test_sorted_ascending(self):
        assert mit.is_sorted([1, 2, 3, 4, 5]) is True

    def test_sorted_descending(self):
        assert mit.is_sorted([5, 4, 3, 2, 1], reverse=True) is True

    def test_not_sorted(self):
        assert mit.is_sorted([1, 3, 2, 4]) is False

    def test_empty(self):
        assert mit.is_sorted([]) is True

    def test_single_element(self):
        assert mit.is_sorted([1]) is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
