#!/usr/bin/env python3
"""Benchmark tabulate vs tabulate_rs"""

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
    print(f"Python tabulate:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust tabulate_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        import tabulate as py_tabulate
    except ImportError:
        print("Installing tabulate...")
        import subprocess
        subprocess.run(["pip", "install", "tabulate", "-q"])
        import tabulate as py_tabulate
    
    try:
        import tabulate_rs
    except ImportError:
        print("ERROR: tabulate_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("TABULATE vs TABULATE_RS BENCHMARK")
    print("="*60)
    
    # Test data - small table
    small_data = [
        ["Alice", 24, "Engineer"],
        ["Bob", 19, "Student"],
        ["Charlie", 35, "Doctor"],
    ]
    small_headers = ["Name", "Age", "Occupation"]
    
    # Test data - medium table
    medium_data = [[f"Row{i}", i, i*1.5, f"Value{i}"] for i in range(50)]
    medium_headers = ["Label", "Int", "Float", "String"]
    
    # Test data - large table
    large_data = [[f"R{i}", i, i*2.5, f"V{i}", i%10] for i in range(200)]
    large_headers = ["A", "B", "C", "D", "E"]

    # Small table - simple format
    py = benchmark("small_simple", lambda: py_tabulate.tabulate(small_data, headers=small_headers, tablefmt="simple"))
    rs = benchmark("small_simple", lambda: tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt="simple"))
    print_comparison(py, rs)
    
    print("\nPython output:")
    print(py_tabulate.tabulate(small_data, headers=small_headers, tablefmt="simple"))
    print("\nRust output:")
    print(tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt="simple"))

    # Small table - grid format
    py = benchmark("small_grid", lambda: py_tabulate.tabulate(small_data, headers=small_headers, tablefmt="grid"))
    rs = benchmark("small_grid", lambda: tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt="grid"))
    print_comparison(py, rs)

    # Small table - github format
    py = benchmark("small_github", lambda: py_tabulate.tabulate(small_data, headers=small_headers, tablefmt="github"))
    rs = benchmark("small_github", lambda: tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt="github"))
    print_comparison(py, rs)
    
    print("\nPython github:")
    print(py_tabulate.tabulate(small_data, headers=small_headers, tablefmt="github"))
    print("\nRust github:")
    print(tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt="github"))

    # Medium table - simple format
    py = benchmark("medium_simple", lambda: py_tabulate.tabulate(medium_data, headers=medium_headers, tablefmt="simple"), iterations=1000)
    rs = benchmark("medium_simple", lambda: tabulate_rs.tabulate(medium_data, headers=medium_headers, tablefmt="simple"), iterations=1000)
    print_comparison(py, rs)

    # Medium table - grid format
    py = benchmark("medium_grid", lambda: py_tabulate.tabulate(medium_data, headers=medium_headers, tablefmt="grid"), iterations=1000)
    rs = benchmark("medium_grid", lambda: tabulate_rs.tabulate(medium_data, headers=medium_headers, tablefmt="grid"), iterations=1000)
    print_comparison(py, rs)

    # Large table - simple format
    py = benchmark("large_simple", lambda: py_tabulate.tabulate(large_data, headers=large_headers, tablefmt="simple"), iterations=500)
    rs = benchmark("large_simple", lambda: tabulate_rs.tabulate(large_data, headers=large_headers, tablefmt="simple"), iterations=500)
    print_comparison(py, rs)

    # Large table - pretty format
    py = benchmark("large_pretty", lambda: py_tabulate.tabulate(large_data, headers=large_headers, tablefmt="pretty"), iterations=500)
    rs = benchmark("large_pretty", lambda: tabulate_rs.tabulate(large_data, headers=large_headers, tablefmt="pretty"), iterations=500)
    print_comparison(py, rs)

    # Test fancy formats
    print("\n" + "="*60)
    print("FORMAT SAMPLES")
    print("="*60)
    
    for fmt in ["rounded_grid", "heavy_grid", "double_grid"]:
        print(f"\n{fmt}:")
        print(tabulate_rs.tabulate(small_data, headers=small_headers, tablefmt=fmt))

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
