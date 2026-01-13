# 🚀 Quick Start Guide - Rusputyn

Get started with Rust-powered Python packages in 5 minutes.

---

## Installation

### From PyPI (Coming Soon)

```bash
pip install validators-rs
pip install humanize-rs
pip install charset-normalizer-rs
# ... more packages
```

### From Source (Current)

```bash
# Clone the repository
git clone https://github.com/Talisberg/rusputyn.git
cd rusputyn

# Install a specific package
cd libraries/validators-rs
pip install maturin
maturin develop --release

# Test it
python -c "import validators_rs; print(validators_rs.email('test@example.com'))"
```

---

## Usage Examples

### Drop-in Replacement Pattern

The beauty of Rusputyn packages is their **100% API compatibility**. Just change your import!

#### Example 1: validators-rs

```python
# Before: Pure Python
import validators

result = validators.email("user@example.com")
# 189,000 ops/sec

# After: Rust-powered
import validators_rs as validators

result = validators.email("user@example.com")
# 9,677,000 ops/sec - 51x faster! ⚡
```

#### Example 2: python-dotenv-rs

```python
# Before: Pure Python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
# 2,000 ops/sec

# After: Rust-powered
from dotenv_rs import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
# 15,000 ops/sec - 7.5x faster! ⚡
```

#### Example 3: humanize-rs

```python
# Before: Pure Python
import humanize

print(humanize.intcomma(1000000))  # "1,000,000"
# 236,000 ops/sec

# After: Rust-powered
import humanize_rs as humanize

print(humanize.intcomma(1000000))  # "1,000,000"
# 15,666,000 ops/sec - 66x faster! ⚡
```

---

## Real-World Use Cases

### Web Application Startup

```python
# app.py - Flask/Django application
import humanize_rs as humanize
import validators_rs as validators
from dotenv_rs import load_dotenv
import os

# Load environment variables (7.5x faster)
load_dotenv()

# Configure app
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Validate configuration (51x faster)
if not validators.url(DATABASE_URL):
    raise ValueError(f"Invalid DATABASE_URL: {DATABASE_URL}")

print(f"✅ App configured successfully!")
```

**Impact:** Application startup reduced from 50ms to 7ms for environment loading.

### Data Processing Pipeline

```python
# process_logs.py
from dateutil_rs import parser
import charset_normalizer_rs as charset

def process_log_file(file_path):
    # Detect encoding (261x faster)
    with open(file_path, 'rb') as f:
        result = charset.from_bytes(f.read())
        encoding = result.best().encoding

    # Parse timestamps (67x faster)
    with open(file_path, encoding=encoding) as f:
        for line in f:
            timestamp_str = line.split()[0]
            timestamp = parser.parse(timestamp_str)
            # Process entry...

# Process 10,000 log files
for log_file in log_files:
    process_log_file(log_file)
```

**Impact:** Pipeline that took 47.7 minutes now takes 11 seconds!

### API Endpoint Validation

```python
# api/views.py
from fastapi import FastAPI, HTTPException
import validators_rs as validators

app = FastAPI()

@app.post("/api/users")
async def create_user(email: str, website: str):
    # Validate email (51x faster)
    if not validators.email(email):
        raise HTTPException(400, "Invalid email")

    # Validate website (58x faster)
    if not validators.url(website):
        raise HTTPException(400, "Invalid URL")

    # Create user...
    return {"status": "success"}
```

**Impact:** API can handle 51x more validation requests per second.

### CLI Tool Output

```python
# cli/stats.py
import tabulate_rs as tabulate
import humanize_rs as humanize

def show_stats(data):
    # Format numbers (66x faster)
    formatted_data = [
        [
            item['name'],
            humanize.intcomma(item['count']),
            humanize.naturalsize(item['bytes']),
        ]
        for item in data
    ]

    # Generate table (11x faster)
    print(tabulate.tabulate(
        formatted_data,
        headers=['Name', 'Count', 'Size'],
        tablefmt='github'
    ))

# Display statistics for 1000 items
show_stats(large_dataset)
```

**Impact:** CLI output generation 11x faster, better user experience.

---

## Package Comparison

| Your Need | Package | Best Use Case | Peak Speedup |
|-----------|---------|---------------|--------------|
| **Config Loading** | python-dotenv-rs | .env files, app startup | 614x |
| **Encoding Detection** | charset-normalizer-rs | Web scraping, file processing | 261x |
| **Date Parsing** | dateutil-rs | APIs, log parsing | 67.9x |
| **Number Formatting** | humanize-rs | UI display, reports | 66.4x |
| **Input Validation** | validators-rs | Form validation, APIs | 79.4x |
| **Table Formatting** | tabulate-rs | CLI tools, reports | 11.4x |
| **Version Parsing** | packaging-rs | Package management | 4.8x |
| **HTML Escaping** | markupsafe-rs | Template rendering | 3.6x |
| **TOML Parsing** | tomli-rs | Config files | 2.5x |
| **Terminal Colors** | colorama-rs | CLI output | 1.3x |

---

## Performance Tips

### 1. Batch Operations
```python
# Less efficient: Individual validations
for email in emails:
    validators_rs.email(email)

# More efficient: Use list comprehension
valid_emails = [e for e in emails if validators_rs.email(e)]
```

### 2. Reuse Parsers
```python
# For dateutil-rs - parser is already fast, but reuse when possible
from dateutil_rs import parser

timestamps = [parser.parse(ts) for ts in timestamp_strings]
```

### 3. Profile Your Code
```python
import time

start = time.perf_counter()
# Your code here
end = time.perf_counter()

print(f"Executed in {(end-start)*1000:.2f}ms")
```

---

## Migration Checklist

Switching from pure Python to Rusputyn? Here's your checklist:

- [ ] Install the Rust-powered package
- [ ] Update imports (usually just add `_rs` suffix)
- [ ] Run your existing tests (should pass without changes)
- [ ] Benchmark the difference
- [ ] Deploy and enjoy the speedup!

### Migration Example

```diff
# requirements.txt
-validators==0.20.0
+validators-rs==0.1.0

# app.py
-import validators
+import validators_rs as validators

# No other changes needed! 🎉
```

---

## Troubleshooting

### Issue: ImportError

```python
ImportError: No module named 'validators_rs'
```

**Solution:** Make sure the package is installed:
```bash
pip install validators-rs  # From PyPI (when available)
# OR
maturin develop --release  # From source
```

### Issue: Performance Not as Expected

**Solution:** Make sure you're using release builds:
```bash
# Development build (slower, for debugging)
maturin develop

# Release build (fast, for production)
maturin develop --release
```

### Issue: API Differences

**Solution:** Rusputyn packages aim for 100% API compatibility. If you find a difference, please [open an issue](https://github.com/Talisberg/rusputyn/issues/new).

---

## Next Steps

1. **Try it yourself:** Install a package and test in your project
2. **Measure the impact:** Use benchmarks to see real gains
3. **Share your results:** Let us know how much faster your code runs!
4. **Vote for more:** Request packages you need in [GitHub Issues](https://github.com/Talisberg/rusputyn/labels/priority-vote)
5. **Contribute:** Help build the next package!

---

## Resources

- **Detailed Benchmarks:** [BENCHMARK_SUMMARY.md](./BENCHMARK_SUMMARY.md)
- **Usage Examples:** [USAGE_EXAMPLES.md](./USAGE_EXAMPLES.md)
- **Performance Results:** [PERFORMANCE.md](./PERFORMANCE.md)
- **Roadmap:** [ROADMAP.md](./ROADMAP.md)
- **Contributing:** [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## Support

- 📧 **Issues:** [GitHub Issues](https://github.com/Talisberg/rusputyn/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Talisberg/rusputyn/discussions)
- ⭐ **Star the repo:** Help others discover Rusputyn!

---

**Making Python blazingly fast, one package at a time! 🚀🦀**
