# validators-rs

High-performance Rust implementation of validators - validate emails, URLs, IPs, and more.

## Overview

`validators-rs` is a Rust-powered Python library that provides fast validation for common data types including emails, URLs, IP addresses, and more.

## Installation

```bash
pip install validators-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- ✅ **Comprehensive Validation**: Email, URL, IP, domain, and more
- 🔄 **Compatible**: Drop-in replacement for the validators library
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Cross-Platform**: Pre-built wheels for Linux, macOS, and Windows

## Quick Start

```python
from validators_rs import email, url, ipv4, domain

# Validate email addresses
print(email("user@example.com"))  # True
print(email("invalid.email"))     # False

# Validate URLs
print(url("https://example.com"))  # True
print(url("not a url"))           # False

# Validate IP addresses
print(ipv4("192.168.1.1"))  # True
print(ipv4("999.999.999.999"))  # False

# Validate domain names
print(domain("example.com"))  # True
print(domain("invalid..domain"))  # False
```

## Available Validators

- `email()`: Validate email addresses
- `url()`: Validate URLs
- `ipv4()`: Validate IPv4 addresses
- `ipv6()`: Validate IPv6 addresses
- `domain()`: Validate domain names
- `mac_address()`: Validate MAC addresses
- `uuid()`: Validate UUIDs
- And more!

## Performance

`validators-rs` provides significant performance improvements over pure Python implementations, making it ideal for high-throughput validation scenarios.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
