# Docker Testing Environment

This Docker environment provides a complete setup for building and testing Rusputyn packages.

## Quick Start

### Build and run interactive shell

```bash
docker compose up -d rusputyn-dev
docker compose exec rusputyn-dev bash
```

### Run all tests

```bash
docker compose run rusputyn-test
```

### Build a specific package

```bash
docker compose exec rusputyn-dev bash
cd libraries/charset-normalizer-rs
maturin develop --release
python3 benchmark.py
```

## What's Included

The Docker image includes:
- Rust 1.75+ toolchain
- Python 3.x with uv (ultra-fast package manager)
- Maturin (for building Rust Python packages)
- All Python dependencies for benchmarking
- Build tools (gcc, etc.)

## Why uv?

This project uses [uv](https://github.com/astral-sh/uv) for Python package management:
- 10-100x faster than pip
- Better dependency resolution
- Built in Rust (fitting for this project!)
- Drop-in replacement for pip commands

## Commands

### Start development environment

```bash
docker compose up -d rusputyn-dev
```

### Enter the container

```bash
docker compose exec rusputyn-dev bash
```

### Stop the environment

```bash
docker compose down
```

### Rebuild after changes

```bash
docker compose build
```

## Testing Individual Packages

Once inside the container:

```bash
# Navigate to a package
cd libraries/packaging-rs

# Build it
maturin develop --release

# Run benchmark
python3 benchmark.py

# Run tests (if available)
pytest tests/
```

## Volume Caching

The setup uses Docker volumes to cache:
- Cargo registry (faster Rust builds)
- Build artifacts (reuse compiled code)

This significantly speeds up subsequent builds.

## Troubleshooting

### Permission issues

If you encounter permission issues with mounted volumes:

```bash
docker compose run --user $(id -u):$(id -g) rusputyn-dev bash
```

### Clean rebuild

```bash
docker compose down -v
docker compose build --no-cache
```

### View logs

```bash
docker compose logs rusputyn-test
```
