#!/usr/bin/env python3
"""
Benchmark python-dotenv vs python-dotenv-rs

Measures performance differences for common .env operations
"""

import time
import tempfile
import os
from io import StringIO

try:
    import dotenv
    PYTHON_AVAILABLE = True
except ImportError:
    PYTHON_AVAILABLE = False
    print("Warning: python-dotenv not installed, comparison benchmarks will be skipped")

try:
    import dotenv_rs
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    print("Error: dotenv_rs not available. Build it first with 'maturin develop --release'")
    exit(1)


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


def test_parse_simple():
    """Benchmark simple .env parsing"""
    content = """
KEY1=value1
KEY2=value2
KEY3=value3
KEY4=value4
KEY5=value5
"""

    print_section("Benchmark: Parse Simple .env (5 variables)")

    iterations = 50000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: dotenv.dotenv_values(stream=StringIO(content)), iterations)
        print(f"Python dotenv:       {py_ops:>10,.0f} ops/sec ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: dotenv_rs.dotenv_values(content), iterations)
    print(f"Rust dotenv_rs:      {rs_ops:>10,.0f} ops/sec ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_parse_complex():
    """Benchmark complex .env with comments and quotes"""
    content = """
# Application Configuration
APP_NAME="My Application"
APP_VERSION='1.0.0'
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_POOL_SIZE=10
DB_TIMEOUT=30

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API Keys
API_KEY="sk-1234567890abcdefghijklmnopqrstuvwxyz"
SECRET_KEY='super-secret-key-do-not-share'

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER="noreply@example.com"
EMAIL_PASSWORD='email-password-123'

# Feature Flags
ENABLE_CACHE=true
ENABLE_LOGGING=true
ENABLE_METRICS=false
"""

    print_section("Benchmark: Parse Complex .env (20 variables with comments)")

    iterations = 20000

    if PYTHON_AVAILABLE:
        py_time, py_ops = benchmark("Python", lambda: dotenv.dotenv_values(stream=StringIO(content)), iterations)
        print(f"Python dotenv:       {py_ops:>10,.0f} ops/sec ({py_time*1000:.2f}ms)")

    rs_time, rs_ops = benchmark("Rust", lambda: dotenv_rs.dotenv_values(content), iterations)
    print(f"Rust dotenv_rs:      {rs_ops:>10,.0f} ops/sec ({rs_time*1000:.2f}ms)")

    if PYTHON_AVAILABLE:
        speedup = rs_ops / py_ops if py_ops > 0 else 0
        print(f"Speedup: {speedup:.1f}x faster")


def test_load_from_file():
    """Benchmark loading from actual file"""
    content = """
DATABASE_URL=postgresql://localhost/mydb
SECRET_KEY=my-secret-key
API_ENDPOINT=https://api.example.com
DEBUG=True
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        print_section("Benchmark: Load from file (.env with 4 variables)")

        iterations = 10000

        if PYTHON_AVAILABLE:
            def py_load():
                dotenv.load_dotenv(temp_path, override=True)
            py_time, py_ops = benchmark("Python", py_load, iterations)
            print(f"Python dotenv:       {py_ops:>10,.0f} ops/sec ({py_time*1000:.2f}ms)")

        def rs_load():
            dotenv_rs.load_dotenv(temp_path, override_vars=True)
        rs_time, rs_ops = benchmark("Rust", rs_load, iterations)
        print(f"Rust dotenv_rs:      {rs_ops:>10,.0f} ops/sec ({rs_time*1000:.2f}ms)")

        if PYTHON_AVAILABLE:
            speedup = py_ops / rs_ops if rs_ops > 0 else 0
            print(f"Speedup: {speedup:.1f}x faster")

    finally:
        os.unlink(temp_path)


def test_set_get_operations():
    """Benchmark set/get key operations"""
    print_section("Benchmark: set_key() and get_key() operations")

    iterations = 100000
    test_key = 'BENCHMARK_TEST_KEY'

    # Benchmark set_key
    if PYTHON_AVAILABLE:
        def py_set():
            dotenv.set_key('.env.temp', test_key, 'test_value')
        py_time, py_ops = benchmark("Python set_key", py_set, iterations // 10)  # Slower, fewer iterations
        print(f"Python set_key:      {py_ops:>10,.0f} ops/sec ({py_time*1000:.2f}ms)")

    def rs_set():
        dotenv_rs.set_key(test_key, 'test_value')
    rs_time, rs_ops = benchmark("Rust set_key", rs_set, iterations)
    print(f"Rust set_key:        {rs_ops:>10,.0f} ops/sec ({rs_time*1000:.2f}ms)")

    # Set a test value for get benchmarks
    os.environ[test_key] = 'test_value'

    # Benchmark get_key
    print()
    if PYTHON_AVAILABLE:
        def py_get():
            dotenv.get_key('.env.temp', test_key)
        py_time, py_ops = benchmark("Python get_key", py_get, iterations // 10)
        print(f"Python get_key:      {py_ops:>10,.0f} ops/sec ({py_time*1000:.2f}ms)")

    def rs_get():
        dotenv_rs.get_key(test_key)
    rs_time, rs_ops = benchmark("Rust get_key", rs_get, iterations)
    print(f"Rust get_key:        {rs_ops:>10,.0f} ops/sec ({rs_time*1000:.2f}ms)")

    # Cleanup
    if test_key in os.environ:
        del os.environ[test_key]
    if os.path.exists('.env.temp'):
        os.unlink('.env.temp')


def main():
    """Run all benchmarks"""
    print("=" * 70)
    print("PYTHON-DOTENV vs DOTENV_RS BENCHMARK")
    print("=" * 70)

    test_parse_simple()
    test_parse_complex()
    test_load_from_file()
    test_set_get_operations()

    print("\n" + "=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
