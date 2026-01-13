# Contributing to Rusputyn

Thank you for your interest in contributing to Rusputyn! This project aims to accelerate Python's ecosystem by providing high-performance Rust implementations of popular Python packages.

## 🎯 Ways to Contribute

### 1. Vote on Package Priorities
Help decide what we build next:
- Browse [priority-vote issues](https://github.com/Talisberg/rusputyn/labels/priority-vote)
- 👍 packages you need
- Comment with your specific use case
- Open new requests: `[VOTE] Package Name - Use Case`

### 2. Test Existing Packages
- Install packages and test in your projects
- Report bugs or compatibility issues
- Share performance benchmarks from your use case
- Suggest API improvements

### 3. Improve Documentation
- Fix typos or unclear explanations
- Add usage examples
- Write tutorials or blog posts
- Create video content
- Translate documentation

### 4. Implement New Packages
Want to implement a package? Great! Follow the guidelines below.

### 5. Optimize Existing Code
- Profile and identify bottlenecks
- Implement algorithmic improvements
- Add SIMD optimizations where applicable
- Reduce memory allocations

---

## 🔧 Development Setup

### Prerequisites
- **Rust 1.75+** - [Install Rust](https://rustup.rs/)
- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **Maturin** - `pip install maturin`
- **Docker** (optional) - For consistent testing environment

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/Talisberg/rusputyn.git
cd rusputyn
```

2. **Pick a package to work on:**
```bash
cd libraries/package-name-rs
```

3. **Build in development mode:**
```bash
maturin develop
```

4. **Build with optimizations:**
```bash
maturin develop --release
```

5. **Run tests:**
```bash
python -m pytest tests/
```

6. **Run benchmarks:**
```bash
python benchmark.py
```

### Using Docker
```bash
# Build the container
docker compose build rusputyn-dev

# Run tests
docker compose run --rm rusputyn-dev bash -c "cd libraries/package-name-rs && python -m pytest"

# Run benchmarks
docker compose run --rm rusputyn-dev bash -c "cd libraries/package-name-rs && python benchmark.py"
```

---

## 📦 Implementing a New Package

### Package Selection Criteria

Ideal packages for Rusputyn:
- ✅ **High download volume** (>100M/month preferred)
- ✅ **Pure Python implementation** (no C extensions)
- ✅ **CPU-intensive operations** (parsing, validation, encoding)
- ✅ **Clear, stable API** (easy to replicate)
- ✅ **Good test coverage** (in original package)

Less ideal:
- ❌ Packages already written in C/Cython
- ❌ Primarily I/O-bound operations
- ❌ Heavy external dependencies
- ❌ Rapidly changing APIs

### Implementation Checklist

#### Phase 1: Setup (1-2 days)
- [ ] Create package directory: `libraries/package-name-rs/`
- [ ] Set up Cargo.toml with PyO3 dependencies
- [ ] Set up pyproject.toml for maturin
- [ ] Copy test files from original package
- [ ] Create basic README.md

#### Phase 2: Core Implementation (3-7 days)
- [ ] Implement core functionality in `src/lib.rs`
- [ ] Expose Python API using PyO3
- [ ] Match original API exactly (function signatures, return types)
- [ ] Handle edge cases and errors
- [ ] Add docstrings

#### Phase 3: Testing (2-3 days)
- [ ] Pass all original package tests
- [ ] Add edge case tests
- [ ] Test error handling
- [ ] Verify API compatibility
- [ ] Test across Python versions (3.8-3.12)

#### Phase 4: Benchmarking (1-2 days)
- [ ] Create comprehensive benchmark suite
- [ ] Compare against original package
- [ ] Test multiple scenarios (small/large inputs)
- [ ] Measure memory usage
- [ ] Document real-world impact

#### Phase 5: Documentation (1 day)
- [ ] Write detailed README with examples
- [ ] Document all public functions
- [ ] Create usage examples
- [ ] Add migration guide
- [ ] Update main project README

### Project Structure Template

```
libraries/package-name-rs/
├── Cargo.toml              # Rust dependencies
├── pyproject.toml          # Python packaging
├── README.md               # Package documentation
├── benchmark.py            # Performance tests
├── src/
│   └── lib.rs             # Main Rust implementation
└── tests/
    └── test_package.py    # Python tests
```

### Cargo.toml Template

```toml
[package]
name = "package-name-rs"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <your.email@example.com>"]
description = "High-performance Rust implementation of package-name"
license = "MIT"

[lib]
name = "package_name_rs"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.20", features = ["extension-module"] }
# Add other dependencies as needed

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true
```

### pyproject.toml Template

```toml
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[project]
name = "package-name-rs"
version = "0.1.0"
description = "High-performance Rust implementation of package-name"
authors = [{name = "Your Name"}]
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Rust",
]

[tool.maturin]
module-name = "package_name_rs"
```

---

## 🧪 Testing Guidelines

### Test Coverage Requirements
- **Minimum:** 90% code coverage
- **All** public functions must have tests
- **Edge cases** must be tested
- **Error handling** must be tested

### Running Tests

```bash
# Run Python tests
python -m pytest tests/ -v

# Run Rust tests (if any)
cargo test

# Check test coverage
python -m pytest tests/ --cov=package_name_rs --cov-report=html
```

### Benchmark Requirements

Every package must include `benchmark.py` with:
- Comparison against original Python package
- Multiple test scenarios (simple, complex, large inputs)
- Operations per second measurement
- Clear output showing speedup

Example benchmark output:
```
==================================================
BENCHMARK: Parse Simple (5 variables)
==================================================
Python:         15,000 ops/sec  (66.7ms)
Rust:        1,060,000 ops/sec  (0.9ms)
Speedup: 70.7x faster
```

---

## 📝 Code Style

### Rust Code Style
- Follow standard Rust formatting: `cargo fmt`
- Run Clippy: `cargo clippy`
- Prefer readability over cleverness
- Add comments for complex logic
- Use meaningful variable names

### Python Code Style
- Follow PEP 8
- Use type hints where applicable
- Write clear docstrings
- Keep test names descriptive

---

## 🔍 Code Review Process

1. **Self-review:** Test thoroughly before submitting
2. **CI checks:** All tests and lints must pass
3. **Peer review:** At least one maintainer approval required
4. **Benchmarks:** Performance gains must be documented
5. **Documentation:** All public APIs must be documented

---

## 📊 Performance Optimization Tips

### General Guidelines
1. **Profile first:** Don't optimize blindly
2. **Algorithm matters:** O(n) vs O(n²) makes huge differences
3. **Reduce allocations:** Reuse buffers where possible
4. **Use appropriate data structures:** HashMap vs Vec
5. **Consider SIMD:** For data-parallel operations

### Common Optimizations
- Use `&str` instead of `String` when possible
- Preallocate vectors with known capacity
- Use `Cow<str>` for copy-on-write semantics
- Leverage Rust's zero-cost abstractions
- Consider using `rayon` for parallelism

### PyO3 Specific
- Minimize Python-Rust boundary crossings
- Batch operations when possible
- Use `#[pyfunction]` for simple functions
- Use `#[pyclass]` for stateful objects
- Release GIL for CPU-intensive work: `py.allow_threads(|| { ... })`

---

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Package:** validators-rs
**Version:** 0.1.0
**Python Version:** 3.11.2
**OS:** macOS 14.0

**Description:**
Brief description of the issue

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Minimal Reproduction:**
\`\`\`python
import validators_rs
# Minimal code to reproduce the issue
\`\`\`

**Additional Context:**
Any other relevant information
```

---

## 💬 Getting Help

- **Discussions:** Use GitHub Discussions for questions
- **Issues:** Check existing issues before creating new ones
- **Discord/Slack:** [Coming soon]

---

## 🎁 Recognition

Contributors will be:
- Listed in the main README
- Credited in package CHANGELOG
- Mentioned in release notes
- Invited to maintainer discussions (for significant contributions)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution helps make Python faster for millions of developers. Whether you're fixing a typo or implementing a new package, your work matters!

**Let's make Python blazingly fast! 🚀**
