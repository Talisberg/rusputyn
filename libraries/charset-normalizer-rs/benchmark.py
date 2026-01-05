#!/usr/bin/env python3
"""Benchmark charset-normalizer vs charset_normalizer_rs"""

import time
import statistics

def benchmark(name, func, iterations=10_000):
    """Run a benchmark and return stats"""
    times = []
    for _ in range(5):
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    mean = statistics.mean(times)
    ops_per_sec = iterations / mean
    
    return {
        'name': name,
        'mean': mean,
        'ops_per_sec': ops_per_sec,
    }

def print_comparison(py_result, rs_result):
    speedup = rs_result['ops_per_sec'] / py_result['ops_per_sec'] if py_result['ops_per_sec'] else 0
    
    print(f"\n{'='*60}")
    print(f"Benchmark: {py_result['name']}")
    print(f"{'='*60}")
    print(f"Python charset-normalizer:  {py_result['ops_per_sec']:>10,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust charset_normalizer_rs: {rs_result['ops_per_sec']:>10,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        from charset_normalizer import from_bytes as py_from_bytes, detect as py_detect
    except ImportError:
        print("Installing charset-normalizer...")
        import subprocess
        subprocess.run(["pip", "install", "charset-normalizer", "-q"])
        from charset_normalizer import from_bytes as py_from_bytes, detect as py_detect
    
    try:
        import charset_normalizer_rs
    except ImportError:
        print("ERROR: charset_normalizer_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("CHARSET-NORMALIZER vs CHARSET_NORMALIZER_RS BENCHMARK")
    print("="*60)
    
    # Test data
    utf8_text = "Hello, World! This is a UTF-8 encoded string with some unicode: café, naïve, 日本語".encode('utf-8')
    latin1_text = "Hello, World! Héllo café naïve".encode('latin-1')
    ascii_text = b"Hello, World! This is plain ASCII text without any special characters."
    mixed_text = b"Some ASCII text with \xff\xfe random bytes"
    
    # Short UTF-8
    py = benchmark("short utf-8", lambda: py_from_bytes(utf8_text))
    rs = benchmark("short utf-8", lambda: charset_normalizer_rs.from_bytes(utf8_text))
    print_comparison(py, rs)
    
    py_result = py_from_bytes(utf8_text).best()
    rs_result = charset_normalizer_rs.from_bytes(utf8_text).best()
    print(f"  Python encoding: {py_result.encoding if py_result else 'None'}")
    print(f"  Rust encoding:   {rs_result.encoding if rs_result else 'None'}")

    # ASCII
    py = benchmark("ascii", lambda: py_from_bytes(ascii_text))
    rs = benchmark("ascii", lambda: charset_normalizer_rs.from_bytes(ascii_text))
    print_comparison(py, rs)

    # Latin-1
    py = benchmark("latin-1", lambda: py_from_bytes(latin1_text))
    rs = benchmark("latin-1", lambda: charset_normalizer_rs.from_bytes(latin1_text))
    print_comparison(py, rs)
    
    py_result = py_from_bytes(latin1_text).best()
    rs_result = charset_normalizer_rs.from_bytes(latin1_text).best()
    print(f"  Python encoding: {py_result.encoding if py_result else 'None'}")
    print(f"  Rust encoding:   {rs_result.encoding if rs_result else 'None'}")

    # Longer UTF-8
    long_utf8 = ("This is a longer text. " * 100).encode('utf-8')
    py = benchmark("long utf-8", lambda: py_from_bytes(long_utf8), iterations=1000)
    rs = benchmark("long utf-8", lambda: charset_normalizer_rs.from_bytes(long_utf8), iterations=1000)
    print_comparison(py, rs)

    # Very long UTF-8
    very_long_utf8 = ("Lorem ipsum dolor sit amet. " * 1000).encode('utf-8')
    py = benchmark("very long utf-8", lambda: py_from_bytes(very_long_utf8), iterations=100)
    rs = benchmark("very long utf-8", lambda: charset_normalizer_rs.from_bytes(very_long_utf8), iterations=100)
    print_comparison(py, rs)

    # detect() function
    print("\n" + "="*60)
    print("DETECT FUNCTION")
    print("="*60)
    
    # Python's detect returns dict, ours returns string
    py = benchmark("detect utf-8", lambda: py_detect(utf8_text))
    rs = benchmark("detect utf-8", lambda: charset_normalizer_rs.detect(utf8_text))
    print_comparison(py, rs)
    
    print(f"  Python: {py_detect(utf8_text)}")
    print(f"  Rust:   {charset_normalizer_rs.detect(utf8_text)}")

    # normalize function (Rust only)
    print("\n" + "="*60)
    print("RUST-ONLY FEATURES")
    print("="*60)
    
    rs = benchmark("normalize", lambda: charset_normalizer_rs.normalize(utf8_text))
    print(f"\nnormalize(): {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  Output: {charset_normalizer_rs.normalize(utf8_text)[:50]}...")

    rs = benchmark("is_valid utf-8", lambda: charset_normalizer_rs.is_valid(utf8_text, "utf-8"))
    print(f"\nis_valid(): {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  is_valid(utf8, 'utf-8'): {charset_normalizer_rs.is_valid(utf8_text, 'utf-8')}")
    print(f"  is_valid(latin1, 'utf-8'): {charset_normalizer_rs.is_valid(latin1_text, 'utf-8')}")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
