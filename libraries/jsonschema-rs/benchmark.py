#!/usr/bin/env python3
"""
Benchmark jsonschema vs jsonschema-rs

Measures performance for JSON Schema validation.
"""

import time
import sys

try:
    import jsonschema as jsonschema_py
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("Warning: jsonschema not installed, comparison benchmarks will be skipped")

try:
    import jsonschema_rs
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("Error: jsonschema_rs not available")
    sys.exit(1)


def benchmark(name, func, iterations=1000):
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


def test_simple_validation():
    """Benchmark simple schema validation"""
    print_section("Benchmark: Simple Object Validation")

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"}
        },
        "required": ["name"]
    }
    data = {"name": "Alice", "age": 30}
    iterations = 1000

    if JSONSCHEMA_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: jsonschema_py.validate(data, schema), iterations)
        print(f"jsonschema:   {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: jsonschema_rs.validate(data, schema), iterations)
    print(f"jsonschema-rs:{rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if JSONSCHEMA_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_complex_schema():
    """Benchmark complex nested schema"""
    print_section("Benchmark: Complex Nested Schema")

    schema = {
        "type": "object",
        "properties": {
            "users": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "minLength": 1},
                        "email": {"type": "string", "format": "email"},
                        "age": {"type": "number", "minimum": 0, "maximum": 150},
                        "address": {
                            "type": "object",
                            "properties": {
                                "street": {"type": "string"},
                                "city": {"type": "string"},
                                "zipcode": {"type": "string", "pattern": "^[0-9]{5}$"}
                            },
                            "required": ["street", "city"]
                        }
                    },
                    "required": ["name", "email"]
                }
            }
        }
    }

    data = {
        "users": [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "zipcode": "12345"
                }
            },
            {
                "name": "Bob",
                "email": "bob@example.com",
                "age": 25,
                "address": {
                    "street": "456 Oak Ave",
                    "city": "Shelbyville",
                    "zipcode": "67890"
                }
            }
        ]
    }
    iterations = 1000

    if JSONSCHEMA_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: jsonschema_py.validate(data, schema), iterations)
        print(f"jsonschema:   {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: jsonschema_rs.validate(data, schema), iterations)
    print(f"jsonschema-rs:{rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if JSONSCHEMA_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_is_valid():
    """Benchmark is_valid (boolean check)"""
    print_section("Benchmark: is_valid() Check")

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "number"}
        }
    }
    data = {"name": "Alice", "age": 30}
    iterations = 10000

    if JSONSCHEMA_AVAILABLE:
        py_validator = jsonschema_py.Draft7Validator(schema)
        py_time, py_ops = benchmark("Python", lambda: py_validator.is_valid(data), iterations)
        print(f"jsonschema:   {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: jsonschema_rs.is_valid(data, schema), iterations)
    print(f"jsonschema-rs:{rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if JSONSCHEMA_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_validator_reuse():
    """Benchmark reusable validator"""
    print_section("Benchmark: Reusable Validator")

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "value": {"type": "number", "minimum": 0}
        },
        "required": ["name", "value"]
    }
    data = {"name": "test", "value": 42}
    iterations = 10000

    if JSONSCHEMA_AVAILABLE:
        py_validator = jsonschema_py.Draft7Validator(schema)
        py_time, py_ops = benchmark("Python", lambda: py_validator.is_valid(data), iterations)
        print(f"jsonschema:   {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_validator = jsonschema_rs.Validator(schema)
    rs_time, rs_ops = benchmark("Rust", lambda: rs_validator.is_valid(data), iterations)
    print(f"jsonschema-rs:{rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if JSONSCHEMA_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_array_validation():
    """Benchmark array validation"""
    print_section("Benchmark: Large Array Validation")

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "name": {"type": "string"}
            },
            "required": ["id", "name"]
        },
        "minItems": 1
    }

    data = [{"id": i, "name": f"item{i}"} for i in range(100)]
    iterations = 100

    if JSONSCHEMA_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: jsonschema_py.validate(data, schema), iterations)
        print(f"jsonschema:   {py_ops:>12,.0f} ops/sec  ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: jsonschema_rs.validate(data, schema), iterations)
    print(f"jsonschema-rs:{rs_ops:>12,.0f} ops/sec  ({rs_time*1000:.2f}ms)")

    if JSONSCHEMA_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def main():
    """Run all benchmarks"""
    print("=" * 70)
    print("JSONSCHEMA vs JSONSCHEMA-RS BENCHMARK")
    print("=" * 70)

    if not JSONSCHEMA_AVAILABLE:
        print("\n⚠️  Running Rust-only benchmarks (no comparison)")

    test_simple_validation()
    test_complex_schema()
    test_is_valid()
    test_validator_reuse()
    test_array_validation()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
