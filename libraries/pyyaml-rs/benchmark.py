#!/usr/bin/env python3
"""
Benchmark pyyaml vs pyyaml-rs

Measures performance for common YAML operations.
"""

import time
import sys

try:
    import yaml as yaml_py
    PYYAML_AVAILABLE = True
except ImportError:
    PYYAML_AVAILABLE = False
    print("Warning: PyYAML not installed, comparison benchmarks will be skipped")

try:
    import pyyaml_rs as yaml_rs
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("Error: pyyaml_rs not available")
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


def test_simple_load():
    """Benchmark simple YAML loading"""
    print_section("Benchmark: safe_load(simple dict)")

    yaml_str = "key: value\nnumber: 42\nflag: true"
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_load(yaml_str), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_load(yaml_str), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_nested_load():
    """Benchmark nested structure loading"""
    print_section("Benchmark: safe_load(nested structure)")

    yaml_str = """
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: secret
  replicas:
    - host: replica1
      port: 5432
    - host: replica2
      port: 5432
"""
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_load(yaml_str), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_load(yaml_str), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_list_load():
    """Benchmark list loading"""
    print_section("Benchmark: safe_load(list)")

    yaml_str = """
- name: Alice
  age: 30
  skills:
    - Python
    - Rust
    - Go
- name: Bob
  age: 25
  skills:
    - JavaScript
    - TypeScript
"""
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_load(yaml_str), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_load(yaml_str), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_load_all():
    """Benchmark multiple document loading"""
    print_section("Benchmark: safe_load_all(3 documents)")

    yaml_str = """---
doc: first
value: 1
---
doc: second
value: 2
---
doc: third
value: 3
"""
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: list(yaml_py.safe_load_all(yaml_str)), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_load_all(yaml_str), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_simple_dump():
    """Benchmark simple dumping"""
    print_section("Benchmark: safe_dump(simple dict)")

    data = {"key": "value", "number": 42, "flag": True}
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_dump(data), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_dump(data), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_nested_dump():
    """Benchmark nested dumping"""
    print_section("Benchmark: safe_dump(nested structure)")

    data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "secret"
            },
            "replicas": [
                {"host": "replica1", "port": 5432},
                {"host": "replica2", "port": 5432}
            ]
        }
    }
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_dump(data), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_dump(data), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_dump_all():
    """Benchmark multiple document dumping"""
    print_section("Benchmark: safe_dump_all(3 documents)")

    docs = [
        {"doc": "first", "value": 1},
        {"doc": "second", "value": 2},
        {"doc": "third", "value": 3}
    ]
    iterations = 10000

    if PYYAML_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: yaml_py.safe_dump_all(docs), iterations)
        print(f"PyYAML:       {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: yaml_rs.safe_dump_all(docs), iterations)
    print(f"pyyaml-rs:    {rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if PYYAML_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def main():
    """Run all benchmarks"""
    print("=" * 70)
    print("PYYAML vs PYYAML-RS BENCHMARK")
    print("=" * 70)

    if not PYYAML_AVAILABLE:
        print("\n⚠️  Running Rust-only benchmarks (no comparison)")

    test_simple_load()
    test_nested_load()
    test_list_load()
    test_load_all()
    test_simple_dump()
    test_nested_dump()
    test_dump_all()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
