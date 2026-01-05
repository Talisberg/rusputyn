#!/usr/bin/env python3
"""
Synthetic Benchmark: Real-World Scenarios Using All 7 Rust Packages

This benchmark demonstrates the combined performance impact of using
all 7 Rust-accelerated packages in realistic workflows.
"""

import time
import random
import string
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Import both Python and Rust versions for comparison
# Note: In practice, you'd install the -rs versions
try:
    import charset_normalizer as charset_py
    import charset_normalizer_rs as charset_rs
    has_charset = True
except ImportError:
    has_charset = False
    print("⚠️  charset-normalizer packages not available")

try:
    import packaging.version as pkg_py
    import packaging_rs.version as pkg_rs
    has_packaging = True
except ImportError:
    has_packaging = False
    print("⚠️  packaging packages not available")

try:
    from dateutil import parser as date_py
    import dateutil_rs as date_rs
    has_dateutil = True
except ImportError:
    has_dateutil = False
    print("⚠️  dateutil packages not available")

try:
    import colorama as color_py
    import colorama_rs as color_rs
    has_colorama = True
except ImportError:
    has_colorama = False
    print("⚠️  colorama packages not available")

try:
    import tabulate as tab_py
    import tabulate_rs as tab_rs
    has_tabulate = True
except ImportError:
    has_tabulate = False
    print("⚠️  tabulate packages not available")

try:
    import humanize as human_py
    import humanize_rs as human_rs
    has_humanize = True
except ImportError:
    has_humanize = False
    print("⚠️  humanize packages not available")

try:
    import validators as valid_py
    import validators_rs as valid_rs
    has_validators = True
except ImportError:
    has_validators = False
    print("⚠️  validators packages not available")


def generate_web_scraping_data(n: int = 1000) -> List[Dict[str, Any]]:
    """Generate synthetic web scraping data."""
    domains = ['example.com', 'test.org', 'demo.net', 'sample.io']
    encodings = [b'\xe4\xb8\xad\xe6\x96\x87', b'\xc3\xa9\xc3\xa0',  # UTF-8
                 b'\xd6\xd0\xce\xc4',  # GBK
                 b'\x92\x86\x8d\x91']  # Shift-JIS
    
    data = []
    for _ in range(n):
        domain = random.choice(domains)
        data.append({
            'url': f'https://{domain}/page{random.randint(1, 1000)}',
            'email': f'user{random.randint(1, 1000)}@{domain}',
            'content': random.choice(encodings) * random.randint(10, 100),
            'timestamp': f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}Z',
            'size': random.randint(1000, 1000000),
        })
    return data


def generate_package_versions(n: int = 500) -> List[str]:
    """Generate synthetic package versions."""
    versions = []
    for _ in range(n):
        major = random.randint(0, 10)
        minor = random.randint(0, 30)
        patch = random.randint(0, 50)
        prerelease = random.choice(['', 'a1', 'b2', 'rc1'])
        versions.append(f"{major}.{minor}.{patch}{prerelease}")
    return versions


def benchmark_web_scraping_pipeline():
    """
    Scenario: Web scraping pipeline
    - Detect charset encoding
    - Parse timestamps
    - Validate URLs and emails
    - Format output table
    """
    print("\n" + "="*80)
    print("SCENARIO 1: Web Scraping Pipeline")
    print("="*80)
    
    data = generate_web_scraping_data(500)
    
    # Python version
    print("\n📦 Python (pure) version:")
    start = time.perf_counter()
    
    results_py = []
    for item in data:
        # Charset detection
        if has_charset:
            encoding = str(charset_py.from_bytes(item['content']).best())
        
        # Date parsing
        if has_dateutil:
            dt = date_py.parse(item['timestamp'])
        
        # Validation
        if has_validators:
            url_valid = valid_py.url(item['url'])
            email_valid = valid_py.email(item['email'])
        
        # Humanize size
        if has_humanize:
            size_human = human_py.naturalsize(item['size'])
        
        results_py.append({
            'url': item['url'][:30],
            'valid': '✓' if (url_valid and email_valid) else '✗',
            'date': dt.strftime('%Y-%m-%d') if has_dateutil else 'N/A',
            'size': size_human if has_humanize else 'N/A'
        })
    
    py_time = time.perf_counter() - start
    
    # Format table
    if has_tabulate:
        table_py = tab_py.tabulate(results_py[:10], headers='keys', tablefmt='grid')
    
    print(f"⏱️  Time: {py_time:.4f}s")
    
    # Rust version
    print("\n🦀 Rust version:")
    start = time.perf_counter()
    
    results_rs = []
    for item in data:
        # Same operations with Rust implementations
        if has_charset:
            encoding = str(charset_rs.from_bytes(item['content']).best())
        
        if has_dateutil:
            dt = date_rs.parse(item['timestamp'])
        
        if has_validators:
            url_valid = valid_rs.url(item['url'])
            email_valid = valid_rs.email(item['email'])
        
        if has_humanize:
            size_human = human_rs.naturalsize(item['size'])
        
        results_rs.append({
            'url': item['url'][:30],
            'valid': '✓' if (url_valid and email_valid) else '✗',
            'date': dt.strftime('%Y-%m-%d') if has_dateutil else 'N/A',
            'size': size_human if has_humanize else 'N/A'
        })
    
    rs_time = time.perf_counter() - start
    
    if has_tabulate:
        table_rs = tab_rs.tabulate(results_rs[:10], headers='keys', tablefmt='grid')
    
    print(f"⏱️  Time: {rs_time:.4f}s")
    print(f"🚀 Speedup: {py_time/rs_time:.2f}x faster")
    
    return py_time, rs_time


def benchmark_package_management():
    """
    Scenario: Package management system
    - Parse version strings
    - Compare versions
    - Sort by version
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Package Management System")
    print("="*80)
    
    versions = generate_package_versions(1000)
    
    # Python version
    print("\n📦 Python (pure) version:")
    start = time.perf_counter()
    
    if has_packaging:
        parsed_py = [pkg_py.Version(v) for v in versions]
        sorted_py = sorted(parsed_py)
        comparisons_py = sum(1 for i in range(len(parsed_py)-1) 
                            if parsed_py[i] < parsed_py[i+1])
    
    py_time = time.perf_counter() - start
    print(f"⏱️  Time: {py_time:.4f}s")
    print(f"   Parsed: {len(versions)} versions")
    
    # Rust version
    print("\n🦀 Rust version:")
    start = time.perf_counter()
    
    if has_packaging:
        parsed_rs = [pkg_rs.Version(v) for v in versions]
        sorted_rs = sorted(parsed_rs)
        comparisons_rs = sum(1 for i in range(len(parsed_rs)-1) 
                            if parsed_rs[i] < parsed_rs[i+1])
    
    rs_time = time.perf_counter() - start
    print(f"⏱️  Time: {rs_time:.4f}s")
    print(f"🚀 Speedup: {py_time/rs_time:.2f}x faster")
    
    return py_time, rs_time


def benchmark_data_dashboard():
    """
    Scenario: Data processing dashboard
    - Humanize large numbers
    - Format timestamps
    - Create tables
    - Validate data
    """
    print("\n" + "="*80)
    print("SCENARIO 3: Data Processing Dashboard")
    print("="*80)
    
    # Generate dashboard data
    metrics = []
    for _ in range(200):
        metrics.append({
            'metric': ''.join(random.choices(string.ascii_uppercase, k=10)),
            'value': random.randint(1000, 1000000000),
            'timestamp': datetime.now() - timedelta(seconds=random.randint(0, 86400)),
            'email': f'user{random.randint(1,100)}@example.com',
        })
    
    # Python version
    print("\n📦 Python (pure) version:")
    start = time.perf_counter()
    
    dashboard_py = []
    for m in metrics:
        if has_humanize:
            value_human = human_py.intcomma(m['value'])
            time_ago = human_py.naturaltime(m['timestamp'])
        
        if has_validators:
            email_valid = valid_py.email(m['email'])
        
        dashboard_py.append({
            'Metric': m['metric'][:10],
            'Value': value_human if has_humanize else str(m['value']),
            'Updated': time_ago if has_humanize else 'N/A',
            'Valid': '✓' if email_valid else '✗'
        })
    
    if has_tabulate:
        table_py = tab_py.tabulate(dashboard_py[:20], headers='keys', tablefmt='pretty')
    
    py_time = time.perf_counter() - start
    print(f"⏱️  Time: {py_time:.4f}s")
    
    # Rust version
    print("\n🦀 Rust version:")
    start = time.perf_counter()
    
    dashboard_rs = []
    for m in metrics:
        if has_humanize:
            value_human = human_rs.intcomma(m['value'])
            time_ago = human_rs.naturaltime(m['timestamp'])
        
        if has_validators:
            email_valid = valid_rs.email(m['email'])
        
        dashboard_rs.append({
            'Metric': m['metric'][:10],
            'Value': value_human if has_humanize else str(m['value']),
            'Updated': time_ago if has_humanize else 'N/A',
            'Valid': '✓' if email_valid else '✗'
        })
    
    if has_tabulate:
        table_rs = tab_rs.tabulate(dashboard_rs[:20], headers='keys', tablefmt='pretty')
    
    rs_time = time.perf_counter() - start
    print(f"⏱️  Time: {rs_time:.4f}s")
    print(f"🚀 Speedup: {py_time/rs_time:.2f}x faster")
    
    return py_time, rs_time


def main():
    print("🦀 RUST PYTHON SPEEDUP SHOWCASE")
    print("Synthetic benchmark combining all 7 Rust-accelerated packages")
    print()
    
    results = {}
    
    # Run benchmarks
    if has_charset and has_dateutil and has_validators and has_humanize and has_tabulate:
        results['web_scraping'] = benchmark_web_scraping_pipeline()
    
    if has_packaging:
        results['package_mgmt'] = benchmark_package_management()
    
    if has_humanize and has_validators and has_tabulate:
        results['dashboard'] = benchmark_data_dashboard()
    
    # Summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)
    
    if results:
        total_py = sum(py for py, _ in results.values())
        total_rs = sum(rs for _, rs in results.values())
        
        print(f"\n📦 Total Python time:  {total_py:.4f}s")
        print(f"🦀 Total Rust time:    {total_rs:.4f}s")
        print(f"🚀 Overall speedup:    {total_py/total_rs:.2f}x faster")
        
        print("\n💡 Key Insight:")
        print("   By combining multiple Rust-accelerated packages, you get")
        print("   compounding performance benefits in real-world applications.")
        print(f"\n   Ecosystem coverage: 2.85 billion downloads/month")
        print(f"   Next targets: pyyaml (575M), click (483M), attrs (442M)")
    else:
        print("\n⚠️  Install the required packages to run the full benchmark:")
        print("   pip install charset-normalizer-rs packaging-rs dateutil-rs")
        print("   pip install colorama-rs tabulate-rs humanize-rs validators-rs")


if __name__ == '__main__':
    main()
