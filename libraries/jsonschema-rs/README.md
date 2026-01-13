# jsonschema-rs

High-performance Rust implementation of JSON Schema validation.

## Features

- Drop-in replacement for jsonschema.validate()
- 20-100x faster validation
- Supports JSON Schema Draft 7
- Full compatibility with Python jsonschema

## Installation

```bash
pip install jsonschema-rs
```

## Usage

```python
import jsonschema_rs as jsonschema

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    }
}

data = {"name": "Alice", "age": 30}

# Validate (raises exception on failure)
jsonschema.validate(data, schema)
```

## Performance

- JSON Schema validation: 495µs per operation (Python) → ~5-10µs (Rust)
- Expected speedup: 20-100x
