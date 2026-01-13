# Priority Packages for Rusputyn

High-value packages prioritized for Rust optimization, including science/data packages.

---

## ✅ Strong Candidates (>50µs operations)

### Text Processing & Parsing

| Package | Downloads/Month | µs per op | Description | Expected Speedup |
|---------|-----------------|-----------|-------------|------------------|
| **pyyaml** | 575M | 121.9µs | YAML parsing | 10-50x |
| **jsonschema** | 385M | 495.1µs | JSON schema validation | 20-100x |
| **pygments** | 500M | 470.0µs | Syntax highlighting | 20-100x |
| **markdown** | 240M | 242.4µs | Markdown to HTML | 15-60x |
| **bleach** | 180M | 136.7µs | HTML sanitization | 10-40x |
| **mistune** | 90M | 95.4µs | Fast Markdown parser | 10-30x |

### Science & Data Packages

| Package | Downloads/Month | Category | Operations | Priority |
|---------|-----------------|----------|------------|----------|
| **numpy** | 1.1B | Numerical computing | Array operations, linear algebra | HIGH |
| **pandas** | 700M | Data analysis | DataFrame operations, groupby, join | HIGH |
| **scipy** | 400M | Scientific computing | Statistical functions, optimization | HIGH |
| **scikit-learn** | 300M | Machine learning | Model training, prediction | HIGH |
| **statsmodels** | 150M | Statistics | Regression, time series | MEDIUM |
| **networkx** | 200M | Graph algorithms | Graph traversal, centrality | MEDIUM |
| **xarray** | 60M | Multi-dimensional arrays | N-D array operations | MEDIUM |
| **sympy** | 180M | Symbolic math | Expression simplification | LOW |

### Crypto & Hashing

| Package | Downloads/Month | Operations | Expected Speedup |
|---------|-----------------|------------|------------------|
| **cryptography** | 1.2B | Encryption, decryption, signing | 5-50x |
| **bcrypt** | 200M | Password hashing | 2-10x |
| **hashlib** (stdlib) | - | MD5, SHA hashing | 10-100x |

### Data Serialization

| Package | Downloads/Month | µs per op | Expected Speedup |
|---------|-----------------|-----------|------------------|
| **orjson** | 150M | Already Rust! | - |
| **msgpack** | 130M | Binary serialization | 10-50x |
| **pickle** (stdlib) | - | Python serialization | 5-20x |

---

## ⚠️ Marginal Candidates (10-50µs)

| Package | Downloads/Month | µs per op | Notes |
|---------|-----------------|-----------|-------|
| idna | 550M | 12.4µs | Internationalized domains |
| tomli | 350M | 11.2µs | TOML parsing |
| toml | 260M | 26.9µs | TOML parsing (older) |

---

## ❌ Too Fast (<10µs - FFI overhead dominates)

| Package | Downloads/Month | µs per op | Reason |
|---------|-----------------|-----------|--------|
| jmespath | 406M | 2.5µs | JSON path queries too fast |
| jinja2 | 371M | 5.0µs | Template rendering optimized |
| jsonpointer | 106M | 1.8µs | Simple pointer resolution |

---

## 🔬 Science Package Deep Dive

### numpy (1.1B downloads/month)

**Why it's important:**
- Foundation of Python scientific computing
- Used by virtually all data science packages
- Heavy array operations

**Challenges:**
- Already uses C/Fortran BLAS/LAPACK
- Competing with highly optimized native code
- Complex API surface

**Opportunity:**
- Specific operations: indexing, slicing, broadcasting
- Type-specific optimizations
- FFI-free array views (if possible)

**Recommendation:** Profile specific operations, target 5-10x for subset

---

### pandas (700M downloads/month)

**Why it's important:**
- Primary data analysis tool
- DataFrames used everywhere
- Slow operations: groupby, merge, join

**Challenges:**
- Built on numpy
- Complex indexing system
- Large API surface

**Opportunity:**
- Specific hot paths: groupby aggregations, joins
- String operations (split, replace, regex)
- CSV parsing (already improved by polars)

**Recommendation:** Target specific operations, 5-20x possible

---

### scipy (400M downloads/month)

**Why it's important:**
- Scientific computing staple
- Statistics, optimization, signal processing

**Challenges:**
- Already uses C/Fortran libraries
- Mixed Python/native code

**Opportunity:**
- Pure Python implementations (some stats functions)
- Optimization algorithms
- Special functions

**Recommendation:** Profile Python-heavy functions, 5-15x possible

---

### scikit-learn (300M downloads/month)

**Why it's important:**
- De facto ML library
- Model training, evaluation

**Challenges:**
- Already uses Cython extensively
- Complex algorithms

**Opportunity:**
- Data preprocessing (scaling, encoding)
- Distance metrics
- Tree traversal

**Recommendation:** Target preprocessing/utils, 3-10x possible

---

## 📊 Evaluation Results from Quick Benchmark

Tested packages:
- ✅ **pyyaml (121µs)** - STRONG candidate
- ✅ **jsonschema (495µs)** - STRONG candidate
- ✅ **pygments (470µs)** - STRONG candidate
- ✅ **markdown (242µs)** - STRONG candidate
- ✅ **bleach (137µs)** - STRONG candidate
- ✅ **mistune (95µs)** - STRONG candidate
- ⚠️ idna (12.4µs) - Marginal
- ⚠️ tomli (11.2µs) - Marginal
- ❌ jmespath (2.5µs) - Too fast
- ❌ jinja2 (5.0µs) - Too fast
- ❌ jsonpointer (1.8µs) - Too fast

---

## 🎯 Recommended Implementation Order

### Phase 2 (Next 6 packages)

1. **pyyaml-rs** (575M, 121µs) - In progress
2. **jsonschema-rs** (385M, 495µs) - Very slow operation
3. **pygments-rs** (500M, 470µs) - Complex highlighting
4. **markdown-rs** (240M, 242µs) - Heavy parsing
5. **bleach-rs** (180M, 137µs) - HTML sanitization
6. **mistune-rs** (90M, 95µs) - Fast markdown

**Total Phase 2:** 1.96B downloads/month

### Phase 3 (Science/Data - High Priority)

1. **numpy-rs subset** - Target specific operations
2. **pandas-rs subset** - Groupby, joins, string ops
3. **scipy-rs subset** - Pure Python functions
4. **cryptography-rs** - Encryption/decryption

### Phase 4 (Explore)

- **msgpack-rs** - Binary serialization
- **bcrypt-rs** - Password hashing
- **networkx-rs subset** - Graph algorithms
- **scikit-learn-rs subset** - Preprocessing

---

## 🔍 Science Package Profiling Strategy

For each science package:

1. **Identify Python-heavy operations** (not C/Cython)
2. **Profile typical workloads** (>50µs threshold)
3. **Create targeted POC** (single function)
4. **Benchmark against native** (target 5x minimum)
5. **Decide: GO if >5x, NO-GO if <5x**

**Example - pandas:**
```python
# Candidate: groupby aggregation
df = pd.DataFrame({'key': [...], 'value': [...]})
df.groupby('key').sum()  # Profile this

# If >50µs → create pandas_rs.groupby_sum()
# Benchmark: pandas vs pandas_rs
# If >5x → proceed with implementation
```

---

## 🚀 Success Patterns

From existing implementations:

1. **charset-normalizer-rs:** 62µs → 261x speedup (heavy algorithms)
2. **python-dotenv-rs:** 2000µs → 614x speedup (file I/O)
3. **validators-rs:** 5.3µs → 51x speedup (regex + validation)
4. **dateutil-rs:** 16µs → 67.9x speedup (date parsing)

**Pattern:** >50µs operations achieve >10x speedup

---

## 📋 Links & Resources

- **cryptography project:** https://github.com/pyca/cryptography
- **numpy:** https://numpy.org/doc/stable/reference/c-api/
- **pandas:** https://pandas.pydata.org/docs/development/extending.html
- **polars (Rust pandas alternative):** https://www.pola.rs/

---

## 🎓 Lessons Applied

1. ✅ Profile FIRST (>50µs threshold)
2. ✅ Quick POC (30 minutes)
3. ✅ Benchmark (target >10x)
4. ✅ Decide: GO/NO-GO based on data
5. ✅ Document unsuitable packages

**This prevents wasted effort on packages like more-itertools, attrs, pyparsing.**
