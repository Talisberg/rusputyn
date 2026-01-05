#!/usr/bin/env python3
"""Benchmark packaging vs packaging_rs"""

import time
import statistics

def benchmark(name, func, iterations=100_000):
    times = []
    for _ in range(5):
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    mean = statistics.mean(times)
    ops_per_sec = iterations / mean
    return {'name': name, 'mean': mean, 'ops_per_sec': ops_per_sec}

def print_comparison(py_result, rs_result):
    speedup = rs_result['ops_per_sec'] / py_result['ops_per_sec'] if py_result['ops_per_sec'] else 0
    print(f"\n{'='*60}")
    print(f"Benchmark: {py_result['name']}")
    print(f"{'='*60}")
    print(f"Python packaging:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust packaging_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        from packaging.version import Version as PyVersion, parse as py_parse
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "packaging", "-q"])
        from packaging.version import Version as PyVersion, parse as py_parse
    
    try:
        from packaging_rs import Version as RsVersion, parse as rs_parse
    except ImportError:
        print("ERROR: packaging_rs not installed")
        return

    print("\n" + "="*60)
    print("PACKAGING vs PACKAGING_RS BENCHMARK")
    print("="*60)
    
    # Parse simple version
    py = benchmark("parse simple", lambda: py_parse("1.0.0"))
    rs = benchmark("parse simple", lambda: rs_parse("1.0.0"))
    print_comparison(py, rs)
    print(f"  Python: {py_parse('1.0.0')}")
    print(f"  Rust:   {rs_parse('1.0.0')}")

    # Parse complex version
    py = benchmark("parse complex", lambda: py_parse("1.0.0a1.post2.dev3+local"))
    rs = benchmark("parse complex", lambda: rs_parse("1.0.0a1.post2.dev3+local"))
    print_comparison(py, rs)

    # Parse with epoch
    py = benchmark("parse epoch", lambda: py_parse("1!2.0.0"))
    rs = benchmark("parse epoch", lambda: rs_parse("1!2.0.0"))
    print_comparison(py, rs)

    # Version comparison
    py_v1, py_v2 = py_parse("1.0.0"), py_parse("2.0.0")
    rs_v1, rs_v2 = rs_parse("1.0.0"), rs_parse("2.0.0")
    
    py = benchmark("compare versions", lambda: py_v1 < py_v2)
    rs = benchmark("compare versions", lambda: rs_v1 < rs_v2)
    print_comparison(py, rs)
    print(f"  1.0.0 < 2.0.0: Python={py_v1 < py_v2}, Rust={rs_v1 < rs_v2}")

    # Pre-release comparison
    py_a, py_b = py_parse("1.0.0a1"), py_parse("1.0.0b1")
    rs_a, rs_b = rs_parse("1.0.0a1"), rs_parse("1.0.0b1")
    
    py = benchmark("compare prerelease", lambda: py_a < py_b)
    rs = benchmark("compare prerelease", lambda: rs_a < rs_b)
    print_comparison(py, rs)
    print(f"  1.0.0a1 < 1.0.0b1: Python={py_a < py_b}, Rust={rs_a < rs_b}")

    # Attribute access
    py_v = py_parse("1.2.3")
    rs_v = rs_parse("1.2.3")
    
    py = benchmark("major attr", lambda: py_v.major)
    rs = benchmark("major attr", lambda: rs_v.major)
    print_comparison(py, rs)
    print(f"  major: Python={py_v.major}, Rust={rs_v.major}")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
