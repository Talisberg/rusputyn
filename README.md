# Rusputyn

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

## Next Targets

**Phase 1: Quick Wins** (targeting +937M downloads/month)

1. **markupsafe-rs** (408M) - HTML/XML escaping - Expected 10-30x speedup
2. **python-dotenv-rs** (273M) - .env file parsing - Expected 5-15x speedup
3. **tomli-rs** (256M) - TOML parser - Expected 3-10x speedup

See [DELIVERABLES.md](./DELIVERABLES.md) for complete roadmap and analysis.

## Performance Philosophy

- **Drop-in compatibility**: 100% API-compatible with original Python packages
- **Real-world speedups**: 10-80x performance improvements on typical workloads
- **Zero-config**: Install and immediately benefit from performance gains
- **Safe**: Leverages Rust's memory safety guarantees

## Getting Started

Each package in `libraries/` is an independent Rust crate with Python bindings via PyO3.

See individual package READMEs for installation and usage instructions.

## Contributing

This is an open-source initiative to accelerate Python's ecosystem. Contributions welcome!

## License

TBD
