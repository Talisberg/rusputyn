#!/usr/bin/env python3
"""Benchmark colorama vs colorama_rs"""

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
    print(f"Python colorama:  {py_result['ops_per_sec']:>12,.0f} ops/sec ({py_result['mean']*1000:.2f}ms)")
    print(f"Rust colorama_rs: {rs_result['ops_per_sec']:>12,.0f} ops/sec ({rs_result['mean']*1000:.2f}ms)")
    print(f"Speedup: {speedup:.1f}x faster")

def main():
    try:
        import colorama
        from colorama import Fore, Back, Style
    except ImportError:
        print("Installing colorama...")
        import subprocess
        subprocess.run(["pip", "install", "colorama", "-q"])
        import colorama
        from colorama import Fore, Back, Style
    
    try:
        import colorama_rs
        from colorama_rs import Fore as ForeRs, Back as BackRs, Style as StyleRs
    except ImportError:
        print("ERROR: colorama_rs not installed. Run 'maturin develop --release' first")
        return

    print("\n" + "="*60)
    print("COLORAMA vs COLORAMA_RS BENCHMARK")
    print("="*60)
    
    # Attribute access benchmarks
    py = benchmark("Fore.RED access", lambda: Fore.RED)
    rs = benchmark("Fore.RED access", lambda: ForeRs.RED)
    print_comparison(py, rs)
    print(f"  Python: {repr(Fore.RED)}")
    print(f"  Rust:   {repr(ForeRs.RED)}")
    print(f"  Match:  {'✓' if Fore.RED == ForeRs.RED else '✗'}")

    py = benchmark("Back.GREEN access", lambda: Back.GREEN)
    rs = benchmark("Back.GREEN access", lambda: BackRs.GREEN)
    print_comparison(py, rs)
    print(f"  Match:  {'✓' if Back.GREEN == BackRs.GREEN else '✗'}")

    py = benchmark("Style.BRIGHT access", lambda: Style.BRIGHT)
    rs = benchmark("Style.BRIGHT access", lambda: StyleRs.BRIGHT)
    print_comparison(py, rs)
    print(f"  Match:  {'✓' if Style.BRIGHT == StyleRs.BRIGHT else '✗'}")

    py = benchmark("Style.RESET_ALL access", lambda: Style.RESET_ALL)
    rs = benchmark("Style.RESET_ALL access", lambda: StyleRs.RESET_ALL)
    print_comparison(py, rs)
    print(f"  Match:  {'✓' if Style.RESET_ALL == StyleRs.RESET_ALL else '✗'}")

    # String concatenation benchmark (common use case)
    py = benchmark("color string build", lambda: Fore.RED + "Hello" + Style.RESET_ALL)
    rs = benchmark("color string build", lambda: ForeRs.RED + "Hello" + StyleRs.RESET_ALL)
    print_comparison(py, rs)
    
    py_str = Fore.RED + "Hello" + Style.RESET_ALL
    rs_str = ForeRs.RED + "Hello" + StyleRs.RESET_ALL
    print(f"  Python: {repr(py_str)}")
    print(f"  Rust:   {repr(rs_str)}")
    print(f"  Match:  {'✓' if py_str == rs_str else '✗'}")

    # Complex string building
    def py_complex():
        return f"{Fore.RED}{Back.WHITE}{Style.BRIGHT}Error:{Style.RESET_ALL} Something went wrong"
    
    def rs_complex():
        return f"{ForeRs.RED}{BackRs.WHITE}{StyleRs.BRIGHT}Error:{StyleRs.RESET_ALL} Something went wrong"
    
    py = benchmark("complex color string", py_complex)
    rs = benchmark("complex color string", rs_complex)
    print_comparison(py, rs)
    print(f"  Match:  {'✓' if py_complex() == rs_complex() else '✗'}")

    # colorize helper function (Rust-only feature)
    print("\n" + "="*60)
    print("RUST-ONLY FEATURES")
    print("="*60)
    
    rs = benchmark("colorize() helper", lambda: colorama_rs.colorize("Hello", fore=ForeRs.RED, style=StyleRs.BRIGHT))
    print(f"\ncolorize() helper: {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  Output: {repr(colorama_rs.colorize('Hello', fore=ForeRs.RED, style=StyleRs.BRIGHT))}")

    # strip_ansi
    colored_text = ForeRs.RED + "Hello " + ForeRs.GREEN + "World" + StyleRs.RESET_ALL
    rs = benchmark("strip_ansi()", lambda: colorama_rs.strip_ansi(colored_text))
    print(f"\nstrip_ansi(): {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  Input:  {repr(colored_text)}")
    print(f"  Output: {repr(colorama_rs.strip_ansi(colored_text))}")

    # 256 color
    rs = benchmark("fore_256()", lambda: colorama_rs.fore_256(196))
    print(f"\nfore_256(): {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  Output: {repr(colorama_rs.fore_256(196))}")

    # RGB color
    rs = benchmark("fore_rgb()", lambda: colorama_rs.fore_rgb(255, 128, 0))
    print(f"\nfore_rgb(): {rs['ops_per_sec']:,.0f} ops/sec")
    print(f"  Output: {repr(colorama_rs.fore_rgb(255, 128, 0))}")

    # Visual demo
    print("\n" + "="*60)
    print("VISUAL DEMO")
    print("="*60)
    print(f"\n{ForeRs.RED}Red text{StyleRs.RESET_ALL}")
    print(f"{ForeRs.GREEN}Green text{StyleRs.RESET_ALL}")
    print(f"{ForeRs.BLUE}Blue text{StyleRs.RESET_ALL}")
    print(f"{StyleRs.BRIGHT}{ForeRs.YELLOW}Bright yellow{StyleRs.RESET_ALL}")
    print(f"{BackRs.RED}{ForeRs.WHITE}White on red{StyleRs.RESET_ALL}")
    print(f"{colorama_rs.fore_rgb(255, 165, 0)}RGB Orange{StyleRs.RESET_ALL}")
    print(f"{colorama_rs.fore_256(201)}256-color Pink{StyleRs.RESET_ALL}")

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
