#!/usr/bin/env python3
"""Benchmark dateutil vs dateutil_rs"""

import time
import statistics
from datetime import datetime

def benchmark(name, func, iterations=50_000):
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
    print(f"Python dateutil:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust dateutil_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        from dateutil import parser as py_parser
    except ImportError:
        print("Installing python-dateutil...")
        import subprocess
        subprocess.run(["pip", "install", "python-dateutil", "-q"])
        from dateutil import parser as py_parser
    
    try:
        import dateutil_rs
    except ImportError:
        print("ERROR: dateutil_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("DATEUTIL vs DATEUTIL_RS BENCHMARK")
    print("="*60)
    
    # Test strings
    test_cases = [
        ("ISO datetime", "2023-01-15T14:30:00"),
        ("ISO with tz", "2023-01-15T14:30:00Z"),
        ("ISO with offset", "2023-01-15T14:30:00+05:30"),
        ("ISO with microseconds", "2023-01-15T14:30:00.123456"),
        ("ISO date only", "2023-01-15"),
        ("US format", "01/15/2023"),
        ("Month name", "January 15, 2023"),
        ("Day month year", "15 January 2023"),
    ]
    
    for name, test_str in test_cases:
        try:
            py = benchmark(name, lambda s=test_str: py_parser.parse(s))
            rs = benchmark(name, lambda s=test_str: dateutil_rs.parse(s))
            print_comparison(py, rs)
            
            py_result = py_parser.parse(test_str)
            rs_result = dateutil_rs.parse(test_str)
            print(f"  Input:  {test_str}")
            print(f"  Python: {py_result}")
            print(f"  Rust:   {rs_result}")
            
            # Compare (ignoring tzinfo differences for now)
            match = (py_result.year == rs_result.year and 
                     py_result.month == rs_result.month and
                     py_result.day == rs_result.day and
                     py_result.hour == rs_result.hour and
                     py_result.minute == rs_result.minute and
                     py_result.second == rs_result.second)
            print(f"  Match:  {'✓' if match else '✗'}")
        except Exception as e:
            print(f"\n{name}: ERROR - {e}")

    # isoparse benchmark (fast path)
    print("\n" + "="*60)
    print("ISOPARSE (fast path)")
    print("="*60)
    
    iso_str = "2023-06-15T10:30:45.123456Z"
    
    try:
        from dateutil.parser import isoparse as py_isoparse
        py = benchmark("isoparse", lambda: py_isoparse(iso_str))
        rs = benchmark("isoparse", lambda: dateutil_rs.isoparse(iso_str))
        print_comparison(py, rs)
    except ImportError:
        print("isoparse not available in this dateutil version")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
