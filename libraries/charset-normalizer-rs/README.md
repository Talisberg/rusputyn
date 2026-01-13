# charset-normalizer-rs

High-performance Rust implementation of charset-normalizer - universal character encoding detection.

## Overview

`charset-normalizer-rs` is a Rust-powered Python library that provides fast and accurate character encoding detection for text files and byte streams.

## Installation

```bash
pip install charset-normalizer-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 🔍 **Accurate Detection**: Reliably detect character encodings
- 🌏 **Universal Support**: Handles encodings from around the world
- 🔄 **Compatible**: Drop-in replacement for charset-normalizer
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from charset_normalizer_rs import from_bytes, from_path

# Detect encoding from bytes
with open('mystery_file.txt', 'rb') as f:
    raw_data = f.read()
    results = from_bytes(raw_data)
    best_match = results.best()
    print(f"Detected encoding: {best_match.encoding}")
    print(f"Decoded text: {str(best_match)}")

# Detect encoding from file path
results = from_path('mystery_file.txt')
best_match = results.best()
print(f"Encoding: {best_match.encoding}")
```

## Common Use Cases

- **File Processing**: Automatically detect and decode text files with unknown encodings
- **Web Scraping**: Handle web content with various character encodings
- **Data Migration**: Convert legacy data with different encodings
- **Log Analysis**: Process log files from different systems and locales

## Supported Encodings

Supports all major character encodings including:
- UTF-8, UTF-16, UTF-32
- ISO-8859 series
- Windows code pages (cp1252, cp1251, etc.)
- Asian encodings (GB2312, Big5, Shift-JIS, etc.)
- And many more!

## Performance

`charset-normalizer-rs` provides significant performance improvements over pure Python implementations, especially when processing large files or analyzing many documents.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
