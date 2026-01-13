#!/usr/bin/env python3
"""
Benchmark more-itertools vs more-itertools-rs

Measures performance for common iterator operations.
"""

import time
import sys

try:
    import more_itertools as mit_py
    PYTHON_AVAILABLE = True
except ImportError:
    PYTHON_AVAILABLE = False
    print("Warning: more-itertools not installed, comparison benchmarks will be skipped")

try:
    import more_itertools_rs as mit_rs
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("Error: more_itertools_rs not available")
    sys.exit(1)


def benchmark(name, func, iterations=10000):
    """Run a benchmark and return ops/sec"""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    end = time.perf_counter()

    duration = end - start
    ops_per_sec = iterations / duration if duration > 0 else 0

    return duration, ops_per_sec


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_chunked():
    """Benchmark chunked operation"""
    print_section("Benchmark: chunked(range(1000), 10)")

    data = list(range(1000))
    iterations = 10000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.chunked(data, 10)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.chunked(data, 10), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_flatten():
    """Benchmark flatten operation"""
    print_section("Benchmark: flatten(nested_lists)")

    data = [[i, i+1, i+2] for i in range(0, 300, 3)]
    iterations = 10000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.flatten(data)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.flatten(data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_take():
    """Benchmark take operation"""
    print_section("Benchmark: take(50, range(1000))")

    data = range(1000)
    iterations = 50000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.take(50, data)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.take(50, data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_unique_everseen():
    """Benchmark unique_everseen operation"""
    print_section("Benchmark: unique_everseen(data with duplicates)")

    data = [i % 100 for i in range(500)]
    iterations = 10000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.unique_everseen(data)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.unique_everseen(data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_partition():
    """Benchmark partition operation"""
    print_section("Benchmark: partition(is_even, range(1000))")

    data = list(range(1000))
    is_even = lambda x: x % 2 == 0
    iterations = 5000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: mit_py.partition(is_even, data), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.partition(is_even, data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_windowed():
    """Benchmark windowed operation"""
    print_section("Benchmark: windowed(range(1000), 5)")

    data = list(range(1000))
    iterations = 5000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.windowed(data, 5)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.windowed(data, 5), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_all_unique():
    """Benchmark all_unique operation"""
    print_section("Benchmark: all_unique()")

    unique_data = list(range(500))
    duplicate_data = [i % 100 for i in range(500)]
    iterations = 20000

    print("\nAll unique (best case):")
    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: mit_py.all_unique(unique_data), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.all_unique(unique_data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")

    print("\nHas duplicates (early exit):")
    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: mit_py.all_unique(duplicate_data), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.all_unique(duplicate_data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_interleave():
    """Benchmark interleave operation"""
    print_section("Benchmark: interleave(3 lists)")

    list1 = list(range(100))
    list2 = list(range(100, 200))
    list3 = list(range(200, 300))
    iterations = 10000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(mit_py.interleave(list1, list2, list3)), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.interleave((list1, list2, list3)), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_first_last():
    """Benchmark first and last operations"""
    print_section("Benchmark: first() and last()")

    data = list(range(1000))
    iterations = 100000

    print("\nfirst():")
    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: mit_py.first(data), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.first(data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")

    print("\nlast():")
    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: mit_py.last(data), iterations)
        print(f"Python:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: mit_rs.last(data), iterations)
    print(f"Rust:         {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def main():
    """Run all benchmarks"""
    print("=" * 70)
    print("MORE-ITERTOOLS vs MORE-ITERTOOLS-RS BENCHMARK")
    print("=" * 70)

    if not PYTHON_AVAILABLE:
        print("\n⚠️  Running Rust-only benchmarks (no comparison)")

    test_chunked()
    test_flatten()
    test_take()
    test_unique_everseen()
    test_partition()
    test_windowed()
    test_all_unique()
    test_interleave()
    test_first_last()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
