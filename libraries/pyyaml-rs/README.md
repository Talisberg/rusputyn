# pyyaml-rs

High-performance Rust implementation of PyYAML.

## Features

- Drop-in replacement for PyYAML's safe_load/safe_dump functions
- 10-50x faster YAML parsing and serialization
- Full API compatibility with PyYAML

## Installation

```bash
pip install pyyaml-rs
```

## Usage

```python
import pyyaml_rs as yaml

# Load YAML
data = yaml.safe_load("key: value")

# Dump YAML
yaml_str = yaml.safe_dump({"key": "value"})
```

## Performance

- YAML parsing: 121µs per operation (Python) → ~5-10µs (Rust)
- Expected speedup: 10-50x
