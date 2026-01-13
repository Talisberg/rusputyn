# packaging-rs

High-performance Rust implementation of packaging - version parsing and comparison utilities.

## Overview

`packaging-rs` is a Rust-powered Python library that provides fast version parsing and comparison, compatible with Python's packaging library but with significantly improved performance.

## Installation

```bash
pip install packaging-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 📦 **Version Handling**: Parse and compare package versions
- 🔄 **Compatible**: Works with PEP 440 version specifications
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from packaging_rs import Version, parse

# Parse versions
v1 = Version("1.2.3")
v2 = Version("2.0.0")
v3 = parse("1.2.3a1")  # Pre-release version

# Compare versions
print(v1 < v2)   # True
print(v2 > v1)   # True
print(v1 == Version("1.2.3"))  # True

# Version information
print(v1.major)  # 1
print(v1.minor)  # 2
print(v1.micro)  # 3
```

## Version Formats

Supports PEP 440 version formats:
- Standard versions: `1.2.3`
- Pre-releases: `1.2.3a1`, `1.2.3b2`, `1.2.3rc1`
- Post-releases: `1.2.3.post1`
- Development releases: `1.2.3.dev1`
- Local versions: `1.2.3+local.version`

## Performance

`packaging-rs` delivers significant performance improvements over pure Python implementations, especially when processing large numbers of version comparisons.

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
