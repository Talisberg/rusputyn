# humanize-rs

High-performance Rust implementation of humanize - turn numbers and dates into human-readable strings.

## Overview

`humanize-rs` is a Rust-powered Python library that makes numbers and dates more human-friendly, providing fast formatting with a simple, intuitive API.

## Installation

```bash
pip install humanize-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 📊 **Number Formatting**: Format large numbers, file sizes, and more
- 🕒 **Time Humanization**: Convert dates to relative time descriptions
- 🔄 **Drop-in Replacement**: Compatible with the humanize library
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from humanize_rs import naturalsize, intcomma, naturaltime
from datetime import datetime, timedelta

# Format file sizes
print(naturalsize(1024))  # "1.0 kB"
print(naturalsize(1024 * 1024))  # "1.0 MB"

# Format large numbers
print(intcomma(1000000))  # "1,000,000"

# Format time differences
now = datetime.now()
past = now - timedelta(hours=2)
print(naturaltime(past))  # "2 hours ago"
```

## Available Functions

- `naturalsize()`: Convert bytes to human-readable file sizes
- `intcomma()`: Add commas to large numbers
- `naturaltime()`: Convert timestamps to relative time
- `scientific()`: Format numbers in scientific notation
- And more!

## Performance

`humanize-rs` delivers significant performance improvements over pure Python implementations, especially when processing large datasets.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
