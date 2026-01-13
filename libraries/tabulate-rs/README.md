# tabulate-rs

High-performance Rust implementation of tabulate - pretty-print tabular data with multiple output formats.

## Overview

`tabulate-rs` is a Rust-powered Python library that provides fast table formatting functionality, compatible with the popular `tabulate` library but with significantly improved performance.

## Installation

```bash
pip install tabulate-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 🔄 **Drop-in Replacement**: Compatible with Python's tabulate library
- 📊 **Multiple Formats**: Support for various table output formats
- 🐍 **Python 3.8+**: Works with Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from tabulate_rs import tabulate

data = [
    ["Alice", 24, "Engineer"],
    ["Bob", 19, "Student"],
    ["Charlie", 30, "Designer"]
]

headers = ["Name", "Age", "Occupation"]

print(tabulate(data, headers=headers, tablefmt="grid"))
```

## Performance

`tabulate-rs` offers significant performance improvements over the pure Python implementation, especially for large datasets.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
