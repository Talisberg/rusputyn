# dateutil-rs

High-performance Rust implementation of python-dateutil - flexible datetime parsing with multiple format support.

## Overview

`dateutil-rs` is a Rust-powered Python library that provides fast datetime parsing functionality, offering compatibility with python-dateutil's parser while delivering significantly improved performance.

## Installation

```bash
pip install dateutil-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 📅 **Flexible Parsing**: Supports multiple date and time formats
- 🔄 **Compatible**: Works with common dateutil patterns
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from dateutil_rs import parse

# Parse various date formats
dt1 = parse("2023-01-15 14:30:00")
dt2 = parse("January 15, 2023")
dt3 = parse("15/01/2023")
dt4 = parse("2023-01-15T14:30:00Z")

print(dt1)  # datetime.datetime(2023, 1, 15, 14, 30, 0)
```

## Supported Formats

- ISO 8601: `2023-01-15T14:30:00Z`
- US Format: `01/15/2023`
- European Format: `15.01.2023`
- Natural Language: `January 15, 2023`
- And many more!

## Performance

`dateutil-rs` provides significant performance improvements over pure Python implementations, especially when parsing large volumes of datetime strings.

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
