# Rusputyn

[![CI](https://github.com/Talisberg/rusputyn/workflows/CI/badge.svg)](https://github.com/Talisberg/rusputyn/actions/workflows/ci.yml)
[![Release](https://github.com/Talisberg/rusputyn/workflows/Release/badge.svg)](https://github.com/Talisberg/rusputyn/actions/workflows/release.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./DOCKER.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.75+-orange.svg)](https://www.rust-lang.org/)

High-performance Rust implementations of popular Python packages, delivering 1.2-614x speedups as drop-in replacements.

## Overview

Rusputyn creates optimized Rust versions of the most popular pure-Python packages from PyPI. These are 100% API-compatible drop-in replacements that dramatically improve performance while maintaining identical functionality.

## Current Status

**10 packages implemented** covering **3.787 billion downloads/month**

| Package | Downloads/Month | Speedup Range | Status |
|---------|-----------------|---------------|--------|
| charset-normalizer-rs | 890M | 4.9x - 327.7x | ✅ Complete |
| packaging-rs | 780M | 1.8x - 4.8x | ✅ Complete |
| dateutil-rs | 717M | 7.3x - 67.9x | ✅ Complete |
| markupsafe-rs | 408M | 1.2x - 3.6x | ✅ Complete |
| colorama-rs | 289M | 1.2x - 1.3x | ✅ Complete |
| python-dotenv-rs | 273M | 16x - 614x | ✅ Complete |
| tomli-rs | 256M | 2.2x - 2.5x | ✅ Complete |
| tabulate-rs | 124M | 6.8x - 11.4x | ✅ Complete |
| humanize-rs | 35M | 2.6x - 66.4x | ✅ Complete |
| validators-rs | 15M | 13.3x - 79.4x | ✅ Complete |

## Project Structure

```
rusputyn/
├── libraries/          # Individual package implementations
│   ├── charset-normalizer-rs/
│   ├── packaging-rs/
│   ├── dateutil-rs/
│   ├── colorama-rs/
│   ├── tabulate-rs/
│   ├── humanize-rs/
│   ├── validators-rs/
│   ├── markupsafe-rs/
│   ├── tomli-rs/
│   └── rust-speedup-showcase/  # Benchmark suite
├── DELIVERABLES.md     # Project analysis and roadmap
└── function_factory.jsx # Build tooling
```

## Roadmap

**Current**: 10 packages (3.787B downloads/month)
**Target**: 21 packages (7.47B downloads/month)

### 🔥 Phase 1 Progress (75% Complete)
1. **markupsafe-rs** (408M) - ✅ Complete
2. **tomli-rs** (256M) - ✅ Complete
3. **python-dotenv-rs** (273M) - ✅ Complete
4. **attrs-rs** (443M) - 📋 Next

**📍 See [ROADMAP.md](./ROADMAP.md) for complete development queue and community voting.**

## Performance Results

**All 10 packages fully benchmarked!** Average of best speedups: **109x faster**

**Top Performers:**
- 🥇 **614x faster** - python-dotenv set_key operations
- 🥈 **261.7x faster** - charset encoding detection
- 🥉 **67.9x faster** - dateutil ISO parsing with timezone

**📊 See [BENCHMARK_SUMMARY.md](./BENCHMARK_SUMMARY.md) for complete results and [BENCHMARKS.csv](./BENCHMARKS.csv) for raw data.**

## Performance Philosophy

- **Drop-in compatibility**: 100% API-compatible with original Python packages
- **Real-world speedups**: 1.2-614x performance improvements on typical workloads
- **Zero-config**: Install and immediately benefit from performance gains
- **Safe**: Leverages Rust's memory safety guarantees

## 🦀 Dual-Ecosystem Design

Rusputyn follows a **core-crate architecture** (like Polars and Pydantic v2):

- **Pure Rust core**: High-performance logic, zero Python dependencies
- **Python bindings**: Thin PyO3 wrapper for Python integration
- **Published to both**: PyPI for Python devs, crates.io for Rust devs

**For Rust Developers:** Every package will be available as a standalone Rust crate. You get battle-tested, production-ready utilities optimized for speed. Coming to crates.io soon.

**For Python Developers:** Same packages you know, 1.2-614x faster, with the confidence that the core logic is being improved by both Python and Rust communities.

## Getting Started

**📚 See [QUICK_START.md](./QUICK_START.md) for detailed installation and usage guides.**

### Quick Example

```python
# Before: Pure Python
import validators
result = validators.email("user@example.com")  # 189K ops/sec

# After: Rust-powered (just change the import!)
import validators_rs as validators
result = validators.email("user@example.com")  # 9.7M ops/sec ⚡

# Same code, same result, 51x faster!
```

### Installation

```bash
pip install validators-rs
```

See [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md) for detailed migration guides and real-world examples.

Each package in `libraries/` is an independent Rust crate with Python bindings via PyO3.

## Contributing

This is an open-source initiative to accelerate Python's ecosystem. We welcome contributions of all kinds!

**🤝 See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on:**
- Testing packages and reporting bugs
- Implementing new packages
- Optimizing existing code
- Improving documentation
- Voting on package priorities

## License

MIT License - see [LICENSE](./LICENSE) file for details
