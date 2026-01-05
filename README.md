# Rusputyn

[![CI](https://github.com/Talisberg/rusputyn/workflows/CI/badge.svg)](https://github.com/Talisberg/rusputyn/actions/workflows/ci.yml)
[![Release](https://github.com/Talisberg/rusputyn/workflows/Release/badge.svg)](https://github.com/Talisberg/rusputyn/actions/workflows/release.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./DOCKER.md)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Rust](https://img.shields.io/badge/rust-1.75+-orange.svg)](https://www.rust-lang.org/)

High-performance Rust implementations of popular Python packages, delivering 10-80x speedups as drop-in replacements.

## Overview

Rusputyn creates optimized Rust versions of the most popular pure-Python packages from PyPI. These are 100% API-compatible drop-in replacements that dramatically improve performance while maintaining identical functionality.

## Current Status

**7 packages implemented** covering **2.85 billion downloads/month**

| Package | Downloads/Month | Speedup Range | Status |
|---------|-----------------|---------------|--------|
| charset-normalizer-rs | 890M | 4.9x - 327.7x | ✅ Complete |
| packaging-rs | 780M | 1.6x - 6.3x | ✅ Complete |
| dateutil-rs | 717M | 9.4x - 85.4x | ✅ Complete |
| colorama-rs | 289M | 1.4x - 1.6x | ✅ Complete |
| tabulate-rs | 124M | 7.6x - 14.1x | ✅ Complete |
| humanize-rs | 35M | 3.7x - 63.7x | ✅ Complete |
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

**Current**: 7 packages (2.85B downloads/month)
**Target**: 21 packages (7.47B downloads/month)

### 🔥 Next Up (Phase 1)
1. **markupsafe-rs** (408M) - 80% complete
2. **tomli-rs** (256M) - 70% complete
3. **python-dotenv-rs** (273M) - Planned
4. **attrs-rs** (443M) - Planned

See [ROADMAP.md](./ROADMAP.md) for complete development queue and community voting.
See [DELIVERABLES.md](./DELIVERABLES.md) for technical analysis.

## Performance Results

**Average speedup: 48x faster** across benchmarked packages

See [PERFORMANCE.md](./PERFORMANCE.md) for detailed benchmark results including:
- **261.7x faster** charset encoding detection
- **66.4x faster** number formatting
- **58.8x faster** URL validation
- Real-world impact analysis

## Performance Philosophy

- **Drop-in compatibility**: 100% API-compatible with original Python packages
- **Real-world speedups**: 10-260x performance improvements on typical workloads
- **Zero-config**: Install and immediately benefit from performance gains
- **Safe**: Leverages Rust's memory safety guarantees

## Getting Started

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

This is an open-source initiative to accelerate Python's ecosystem. Contributions welcome!

## License

TBD
