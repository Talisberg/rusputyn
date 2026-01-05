#!/usr/bin/env python3
"""Benchmark validators vs validators_rs"""

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
    print(f"Python validators:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust validators_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        import validators
    except ImportError:
        print("Installing validators...")
        import subprocess
        subprocess.run(["pip", "install", "validators", "-q"])
        import validators
    
    try:
        import validators_rs
    except ImportError:
        print("ERROR: validators_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("VALIDATORS vs VALIDATORS_RS BENCHMARK")
    print("="*60)
    
    # Test values
    test_email = "test@example.com"
    test_url = "https://www.example.com/path?query=1"
    test_domain = "example.com"
    test_ipv4 = "192.168.1.1"
    test_ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    test_uuid = "550e8400-e29b-41d4-a716-446655440000"
    test_slug = "my-awesome-slug-123"
    test_md5 = "d41d8cd98f00b204e9800998ecf8427e"
    test_mac = "01:23:45:67:89:AB"
    test_card = "4111111111111111"

    # email benchmark
    py = benchmark("email", lambda: validators.email(test_email))
    rs = benchmark("email", lambda: validators_rs.email(test_email))
    print_comparison(py, rs)
    print(f"  Python: {validators.email(test_email)}")
    print(f"  Rust:   {validators_rs.email(test_email)}")

    # url benchmark
    py = benchmark("url", lambda: validators.url(test_url))
    rs = benchmark("url", lambda: validators_rs.url(test_url))
    print_comparison(py, rs)
    print(f"  Python: {validators.url(test_url)}")
    print(f"  Rust:   {validators_rs.url(test_url)}")

    # domain benchmark
    py = benchmark("domain", lambda: validators.domain(test_domain))
    rs = benchmark("domain", lambda: validators_rs.domain(test_domain))
    print_comparison(py, rs)
    print(f"  Python: {validators.domain(test_domain)}")
    print(f"  Rust:   {validators_rs.domain(test_domain)}")

    # ipv4 benchmark
    py = benchmark("ipv4", lambda: validators.ipv4(test_ipv4))
    rs = benchmark("ipv4", lambda: validators_rs.ipv4(test_ipv4))
    print_comparison(py, rs)
    print(f"  Python: {validators.ipv4(test_ipv4)}")
    print(f"  Rust:   {validators_rs.ipv4(test_ipv4)}")

    # ipv6 benchmark
    py = benchmark("ipv6", lambda: validators.ipv6(test_ipv6))
    rs = benchmark("ipv6", lambda: validators_rs.ipv6(test_ipv6))
    print_comparison(py, rs)
    print(f"  Python: {validators.ipv6(test_ipv6)}")
    print(f"  Rust:   {validators_rs.ipv6(test_ipv6)}")

    # uuid benchmark
    py = benchmark("uuid", lambda: validators.uuid(test_uuid))
    rs = benchmark("uuid", lambda: validators_rs.uuid(test_uuid))
    print_comparison(py, rs)
    print(f"  Python: {validators.uuid(test_uuid)}")
    print(f"  Rust:   {validators_rs.uuid(test_uuid)}")

    # slug benchmark
    py = benchmark("slug", lambda: validators.slug(test_slug))
    rs = benchmark("slug", lambda: validators_rs.slug(test_slug))
    print_comparison(py, rs)
    print(f"  Python: {validators.slug(test_slug)}")
    print(f"  Rust:   {validators_rs.slug(test_slug)}")

    # md5 benchmark
    py = benchmark("md5", lambda: validators.md5(test_md5))
    rs = benchmark("md5", lambda: validators_rs.md5(test_md5))
    print_comparison(py, rs)
    print(f"  Python: {validators.md5(test_md5)}")
    print(f"  Rust:   {validators_rs.md5(test_md5)}")

    # mac_address benchmark
    py = benchmark("mac_address", lambda: validators.mac_address(test_mac))
    rs = benchmark("mac_address", lambda: validators_rs.mac_address(test_mac))
    print_comparison(py, rs)
    print(f"  Python: {validators.mac_address(test_mac)}")
    print(f"  Rust:   {validators_rs.mac_address(test_mac)}")

    # card_number benchmark
    py = benchmark("card_number", lambda: validators.card_number(test_card))
    rs = benchmark("card_number", lambda: validators_rs.card_number(test_card))
    print_comparison(py, rs)
    print(f"  Python: {validators.card_number(test_card)}")
    print(f"  Rust:   {validators_rs.card_number(test_card)}")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
