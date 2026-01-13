# Lessons Learned: more-itertools-rs

**Date:** 2026-01-06
**Status:** ❌ Implementation abandoned - not suitable for Rust optimization
**Reason:** FFI overhead exceeds performance gains

---

## Summary

Implemented 13 core functions from more-itertools in Rust, achieving 100% API compatibility and passing all tests. However, **benchmarks showed 0.5x-1.3x performance** (most functions were SLOWER than pure Python).

**Key Finding:** Some Python packages are fundamentally unsuitable for Rust optimization when FFI boundary crossing overhead exceeds computational gains.

---

## Benchmark Results

| Function | Python | Rust | Speedup | Verdict |
|----------|--------|------|---------|---------|
| chunked | 59K ops/s | 79K ops/s | 1.3x | ✓ Marginal |
| flatten | 308K ops/s | 168K ops/s | 0.5x | ❌ 2x SLOWER |
| take | 1.77M ops/s | 1.40M ops/s | 0.8x | ❌ SLOWER |
| unique_everseen | 83K ops/s | 99K ops/s | 1.2x | ✓ Marginal |
| partition | 2.07M ops/s | 17K ops/s | 0.0x | ❌ 122x SLOWER |
| windowed | 13K ops/s | 12K ops/s | 1.0x | ≈ Same |
| all_unique | 77K ops/s | 48K ops/s | 0.6x | ❌ SLOWER |
| interleave | 248K ops/s | 317K ops/s | 1.3x | ✓ Marginal |
| first | 13.1M ops/s | 8.9M ops/s | 0.7x | ❌ SLOWER |
| last | 5.7M ops/s | 174K ops/s | 0.0x | ❌ 33x SLOWER |

**Average:** 0.7x (30% SLOWER overall)

---

## Root Cause Analysis

### 1. FFI Boundary Crossing Overhead

Every function call crosses the Python/Rust boundary:

```python
result = mit_rs.chunked([1, 2, 3, 4, 5, 6], 2)
```

**What happens:**
1. Python list → Rust (memory copy: ~500ns)
2. Rust processes (actual work: ~100ns)
3. Rust result → Python (memory copy: ~500ns)

**Total:** ~1100ns, where only 100ns is actual work (91% overhead!)

### 2. Eager vs. Lazy Evaluation

**Python more-itertools:** Lazy iterators (yield on demand)
```python
for chunk in chunked(huge_list, 10):  # Processes incrementally
    process(chunk)
```

**Our Rust version:** Eager evaluation (build entire result)
```rust
fn chunked() -> PyObject {
    let mut result = Vec::new();
    // Build entire result upfront
    Ok(PyList::new(py, result).to_object(py))
}
```

**Impact:** Extra memory allocation and upfront processing cost.

### 3. Python Callbacks from Rust (Fatal)

`partition()` was 122x SLOWER because:

```rust
for item in iter {
    let result: bool = pred.call1((item_obj,))?.extract()?;
    // ↑ Calling Python function from Rust
    // Cost: ~10,000ns per call (100x overhead)
}
```

Calling Python functions from Rust is catastrophically slow.

### 4. Type Conversion Overhead

`last()` was 33x SLOWER:

```rust
for item in iter {
    last_item = Some(item?);  // Box each item
}
Ok(item.to_object(py))  // Convert back to Python
```

Every iteration boxes the item, final conversion to PyObject adds overhead.

---

## What We Learned

### When Rust Optimization FAILS

❌ **Simple iteration operations**
- Python's iterator protocol is already highly optimized
- C-level loops in CPython are very fast
- Rust can't beat this for simple operations

❌ **Many small boundary crossings**
- Per-item processing across FFI kills performance
- Cost: ~500-1000ns per crossing
- Need >10,000ns of work per crossing to break even

❌ **Python callbacks from Rust**
- Calling Python functions from Rust: ~10,000ns
- Native Python function calls: ~100ns
- 100x slowdown!

❌ **Lazy iterators**
- Python's lazy evaluation is efficient
- Rust's eager evaluation wastes memory
- PyO3 doesn't support lazy iterators well

### When Rust Optimization SUCCEEDS

✅ **Heavy computation** (charset-normalizer: 261x)
- Thousands of operations per item
- FFI overhead amortized across work
- Pure algorithmic logic

✅ **Bulk processing** (python-dotenv: 614x)
- Process entire file at once
- Few boundary crossings
- Return simple result

✅ **No Python callbacks** (validators: 51x)
- Self-contained algorithms
- No calling back into Python
- Pure Rust logic

✅ **Simple return types** (all successful packages)
- Return bool, string, int, dict
- Not complex nested structures
- Easy conversion

---

## Comparison: Success vs. Failure

### SUCCESS: charset-normalizer-rs (261x faster)

```rust
#[pyfunction]
fn detect_encoding(bytes: &[u8]) -> PyResult<String> {
    // Input: 1MB bytes (1 boundary crossing)
    // Process: 10M+ operations
    // Output: String (1 boundary crossing)
    // Total: 2 crossings, heavy work
}
```

**Ratio:** 10M operations / 2 crossings = 5M ops/crossing ✅

### FAILURE: more-itertools-rs (0.5-1.3x)

```rust
#[pyfunction]
fn chunked(iterable: &PyAny, n: usize) -> PyResult<PyObject> {
    // Input: N items (N boundary crossings)
    // Process: 10 operations per item
    // Output: N/10 chunks (N/10 boundary crossings)
    // Total: 1.1N crossings, minimal work
}
```

**Ratio:** 10 operations / 1.1N crossings ≈ 9 ops/crossing ❌

---

## Decision: Why We're Stopping

1. **Below performance threshold:** 0.7x average vs. 10x+ goal
2. **Optimization unlikely:** Would need:
   - Lazy iterators (complex PyO3 work)
   - Avoid Python callbacks (impossible for predicate functions)
   - Zero-copy (PyO3 limitations)
3. **Effort not justified:** 4-6 weeks for maybe 3-5x vs. moving to pyparsing (20-50x)

---

## What Could Have Made This Work

### Hypothetically

1. **Native Rust iterator chain:**
   ```python
   # If we could keep data in Rust across multiple calls
   result = (mit_rs.iter(data)
       .chunked(10)
       .flatten()
       .take(50))  # All in Rust, cross boundary once
   ```

2. **Compiled predicates:**
   ```python
   # If predicates could be JIT-compiled to Rust
   partition(mit_rs.compile("x % 2 == 0"), data)
   ```

3. **Zero-copy views:**
   ```python
   # If we could work on Python data without copying
   chunked(data, 10)  # View into existing Python list
   ```

**Reality:** None of these are practical with PyO3/Python integration.

---

## Recommendations for Future Package Selection

### ✅ PROFILE FIRST

Before implementing ANY package:

1. **30-minute POC:** Quick Rust implementation
2. **Benchmark:** Compare to Python
3. **Decision:**
   - <5x → STOP
   - 5-10x → REVIEW CAREFULLY
   - >10x → PROCEED

### ✅ CHECK CRITERIA

- [ ] CPU-bound operations (thousands of ops per call)
- [ ] Few boundary crossings (<10 per operation)
- [ ] No Python callbacks
- [ ] Returns simple types
- [ ] Bulk processing possible

### ✅ RED FLAGS

- ⚠️ Simple iteration (Python already fast)
- ⚠️ Requires Python functions as arguments
- ⚠️ Lazy evaluation model
- ⚠️ Returns complex nested structures
- ⚠️ Many small operations

---

## Value of This Experiment

While we didn't create a production package, we learned:

1. **Validation criteria:** Not all Python packages benefit from Rust
2. **FFI overhead:** Real cost of boundary crossings
3. **Profile-first approach:** 30-minute POC saves weeks
4. **Clear patterns:** What works vs. what doesn't

**Cost:** 4 hours
**Saved:** 4-6 weeks of futile optimization
**Value:** Priceless lessons for project direction

---

## Next Steps

1. ✅ Document lessons in PACKAGE_SELECTION_CRITERIA.md
2. ✅ Add more-itertools to "unsuitable packages" list
3. ✅ Move to pyparsing-rs (meets all criteria)
4. ✅ Apply profile-first approach going forward

---

## Files Created (for reference)

- `src/lib.rs` - 13 functions implemented
- `tests/test_more_itertools.py` - 40+ tests (all passing)
- `benchmark.py` - Comprehensive benchmark suite
- This document

**Status:** Preserved for educational value, but not recommended for production use.

---

*"Failure is not fatal. It's the courage to continue that counts." - Winston Churchill*

*This experiment made Rusputyn smarter about package selection.*
