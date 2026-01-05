#!/usr/bin/env python3
"""Benchmark humanize vs humanize_rs"""

import time
import statistics

def benchmark(name, func, iterations=100_000):
    """Run a benchmark and return stats"""
    times = []
    for _ in range(5):
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    
    mean = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0
    ops_per_sec = iterations / mean
    
    return {
        'name': name,
        'mean': mean,
        'stdev': stdev,
        'ops_per_sec': ops_per_sec,
        'iterations': iterations
    }

def print_comparison(py_result, rs_result):
    """Print comparison between Python and Rust results"""
    speedup = py_result['ops_per_sec'] / rs_result['ops_per_sec'] if rs_result['ops_per_sec'] else 0
    speedup = rs_result['ops_per_sec'] / py_result['ops_per_sec'] if py_result['ops_per_sec'] else 0
    
    print(f"\n{'='*60}")
    print(f"Benchmark: {py_result['name']}")
    print(f"{'='*60}")
    print(f"Python humanize:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust humanize_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        import humanize
    except ImportError:
        print("Installing humanize...")
        import subprocess
        subprocess.run(["pip", "install", "humanize", "-q"])
        import humanize
    
    try:
        import humanize_rs
    except ImportError:
        print("ERROR: humanize_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("HUMANIZE vs HUMANIZE_RS BENCHMARK")
    print("="*60)
    
    # Test values
    test_int = 1_234_567_890
    test_size = 1_048_576  # 1 MB
    
    # intcomma benchmark
    py = benchmark("intcomma", lambda: humanize.intcomma(test_int))
    rs = benchmark("intcomma", lambda: humanize_rs.intcomma(test_int))
    print_comparison(py, rs)
    
    # Verify correctness
    py_result = humanize.intcomma(test_int)
    rs_result = humanize_rs.intcomma(test_int)
    print(f"  Python output: {py_result}")
    print(f"  Rust output:   {rs_result}")
    print(f"  Match: {'✓' if py_result == rs_result else '✗'}")
    
    # ordinal benchmark  
    py = benchmark("ordinal", lambda: humanize.ordinal(test_int))
    rs = benchmark("ordinal", lambda: humanize_rs.ordinal(test_int))
    print_comparison(py, rs)
    
    py_result = humanize.ordinal(test_int)
    rs_result = humanize_rs.ordinal(test_int)
    print(f"  Python output: {py_result}")
    print(f"  Rust output:   {rs_result}")
    print(f"  Match: {'✓' if py_result == rs_result else '✗'}")
    
    # naturalsize benchmark
    py = benchmark("naturalsize", lambda: humanize.naturalsize(test_size))
    rs = benchmark("naturalsize", lambda: humanize_rs.naturalsize(test_size))
    print_comparison(py, rs)
    
    py_result = humanize.naturalsize(test_size)
    rs_result = humanize_rs.naturalsize(test_size)
    print(f"  Python output: {py_result}")
    print(f"  Rust output:   {rs_result}")
    
    # intword benchmark
    py = benchmark("intword", lambda: humanize.intword(test_int))
    rs = benchmark("intword", lambda: humanize_rs.intword(test_int))
    print_comparison(py, rs)
    
    py_result = humanize.intword(test_int)
    rs_result = humanize_rs.intword(test_int)
    print(f"  Python output: {py_result}")
    print(f"  Rust output:   {rs_result}")
    
    # apnumber benchmark
    py = benchmark("apnumber", lambda: humanize.apnumber(5))
    rs = benchmark("apnumber", lambda: humanize_rs.apnumber(5))
    print_comparison(py, rs)
    
    py_result = humanize.apnumber(5)
    rs_result = humanize_rs.apnumber(5)
    print(f"  Python output: {py_result}")
    print(f"  Rust output:   {rs_result}")
    print(f"  Match: {'✓' if py_result == rs_result else '✗'}")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
