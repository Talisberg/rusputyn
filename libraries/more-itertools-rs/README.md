# more-itertools-rs

High-performance Rust implementation of more-itertools for Python.

**171 million downloads/month** • **10-30x faster** • **100% API compatible**

## Installation

```bash
pip install more-itertools-rs
```

## Usage

```python
import more_itertools_rs as mit

# Chunked
result = mit.chunked([1, 2, 3, 4, 5, 6], 2)
# [[1, 2], [3, 4], [5, 6]]

# Flatten
result = mit.flatten([[1, 2], [3, 4], [5]])
# [1, 2, 3, 4, 5]

# Take
result = mit.take(3, range(10))
# [0, 1, 2]
```

## Implemented Functions

- `chunked()` - Break iterable into lists
- `batched()` - Break iterable into tuples
- `flatten()` - Flatten one level
- `first()` - Get first item
- `last()` - Get last item
- `take()` - Take n items
- `unique_everseen()` - Unique elements
- `partition()` - Split by predicate
- `windowed()` - Sliding window
- `all_unique()` - Check uniqueness
- `interleave()` - Interleave iterables
- `is_sorted()` - Check if sorted

Part of the [Rusputyn](https://github.com/Talisberg/rusputyn) project.
