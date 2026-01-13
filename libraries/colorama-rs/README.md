# colorama-rs

High-performance Rust implementation of colorama - cross-platform colored terminal text.

## Overview

`colorama-rs` is a Rust-powered Python library for producing colored terminal text and cursor positioning, offering cross-platform support with enhanced performance.

## Installation

```bash
pip install colorama-rs
```

## Features

- 🚀 **High Performance**: Built with Rust for maximum speed
- 🎨 **Colored Output**: Easy-to-use API for colored text
- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🔄 **Compatible**: Drop-in replacement for colorama
- 🐍 **Python 3.8+**: Supports Python 3.8 through 3.14
- 🌍 **Pre-built Wheels**: Available for all major platforms

## Quick Start

```python
from colorama_rs import Fore, Back, Style

# Print colored text
print(Fore.RED + 'Red text')
print(Fore.GREEN + 'Green text')
print(Back.BLUE + 'Blue background')
print(Style.BRIGHT + 'Bright text' + Style.RESET_ALL)

# Combine colors
print(Fore.YELLOW + Back.BLUE + 'Yellow on blue' + Style.RESET_ALL)
```

## Available Colors

### Foreground Colors
- BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
- LIGHTBLACK_EX, LIGHTRED_EX, LIGHTGREEN_EX, etc.

### Background Colors
- Same as foreground colors but with `Back.` prefix

### Styles
- BRIGHT, DIM, NORMAL, RESET_ALL

## Cross-Platform Support

`colorama-rs` automatically handles Windows console API calls and ANSI codes on other platforms, providing a consistent experience across all operating systems.

## Performance

Built with Rust, `colorama-rs` offers improved performance over the pure Python implementation, especially for applications with heavy terminal output.

## License

BSD License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
