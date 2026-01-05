# Target Package Analysis

## Selection Criteria

1. **Impact Score** = (Monthly Downloads) / (Implementation Complexity)
2. **Pure Python** = No C extensions, no native dependencies
3. **CPU-Bound** = Performance-critical operations that benefit from Rust

## Top 15 Targets (Ranked by Impact)

### Tier 1: High Impact, Low-Medium Complexity ⭐⭐⭐

| Rank | Package | Downloads/mo | Complexity | Impact Score | Priority |
|------|---------|--------------|------------|--------------|----------|
| 1 | **markupsafe** | 408M | Low | 🔥🔥🔥 | **NEXT** |
| 2 | **python-dotenv** | 273M | Low | 🔥🔥🔥 | **NEXT** |
| 3 | **tomli** | 256M | Low | 🔥🔥🔥 | High |
| 4 | **text-unidecode** | 48M | Low | 🔥🔥 | Medium |

**Why these first?**
- Simple APIs, single-purpose libraries
- Clear performance bottlenecks (string operations)
- Quick implementation (1-2 days each)
- High adoption potential (drop-in replacements)

### Tier 2: High Impact, Medium Complexity ⭐⭐

| Rank | Package | Downloads/mo | Complexity | Impact Score | Notes |
|------|---------|--------------|------------|--------------|-------|
| 5 | **pyyaml** | 575M | Medium | 🔥🔥 | Parser implementation |
| 6 | **click** | 483M | Medium | 🔥🔥 | CLI framework |
| 7 | **jmespath** | 405M | Medium | 🔥🔥 | JSON query language |
| 8 | **pytz** | 377M | Low-Med | 🔥🔥 | Timezone handling |
| 9 | **tqdm** | 261M | Medium | 🔥🔥 | Progress bars |
| 10 | **pyparsing** | 228M | Medium | 🔥🔥 | Parser combinator |
| 11 | **more-itertools** | 170M | Medium | 🔥 | Iterator utilities |
| 12 | **python-multipart** | 140M | Medium | 🔥 | HTTP multipart |
| 13 | **jsonpointer** | 106M | Low-Med | 🔥 | JSON navigation |
| 14 | **croniter** | 41M | Medium | 🔥 | Cron iteration |
| 15 | **arrow** | 54M | Medium | 🔥 | Datetime library |

### Tier 3: High Impact, High Complexity ⭐

| Package | Downloads/mo | Why Complex | Decision |
|---------|--------------|-------------|----------|
| **jinja2** | 370M | Templating engine, large API | Later |
| **attrs** | 442M | Metaclass magic, introspection | Later |
| **rich** | 264M | Complex rendering, many features | Later |

## Detailed Analysis: Next 4 Targets

### 1. markupsafe (408M downloads/month) 🎯

**What it does:** HTML/XML string escaping and SafeString wrapper

**Core functions:**
- `escape(s)` - Escape HTML special chars
- `escape_silent(s)` - Escape with None handling
- `soft_unicode(s)` - Coerce to unicode
- `Markup` class - Safe string wrapper

**Why Rust wins:**
- Heavy string processing
- Byte-level operations
- Zero-copy optimizations possible

**Expected speedup:** 10-30x for escape operations

**Implementation time:** 1-2 days

**API surface:** Small, well-defined

---

### 2. python-dotenv (273M downloads/month) 🎯

**What it does:** Parse .env files and load into environment

**Core functions:**
- `load_dotenv()` - Load .env file
- `dotenv_values()` - Parse to dict
- `find_dotenv()` - Locate .env file
- Variable interpolation

**Why Rust wins:**
- File I/O and parsing
- String manipulation
- Pattern matching

**Expected speedup:** 5-15x for parsing

**Implementation time:** 1-2 days

**API surface:** Small, focused

---

### 3. tomli (256M downloads/month) 🎯

**What it does:** TOML parser (read-only, Python 3.11+ uses it)

**Core functions:**
- `loads(s)` - Parse TOML string
- `load(fp)` - Parse TOML file

**Why Rust wins:**
- Parser implementation
- Can use existing toml-rs crate
- Critical for Python 3.11+ (used in stdlib fallback)

**Expected speedup:** 3-10x for parsing

**Implementation time:** 2-3 days

**API surface:** Minimal (2 functions)

---

### 4. text-unidecode (48M downloads/month)

**What it does:** Transliterate Unicode text to ASCII

**Core functions:**
- `unidecode(s)` - Convert unicode to ASCII

**Why Rust wins:**
- Unicode normalization
- Character mapping
- String transformations

**Expected speedup:** 8-20x

**Implementation time:** 1-2 days

**API surface:** Single function

---

## Implementation Strategy

### Phase 1: Quick Wins (1-2 weeks)
1. ✅ markupsafe-rs
2. ✅ python-dotenv-rs
3. ✅ tomli-rs
4. ✅ text-unidecode-rs

**Total reach:** 985M downloads/month
**Combined total:** 3.8B downloads/month

### Phase 2: Medium Complexity (2-4 weeks)
5. pyyaml-rs (575M)
6. pytz-rs (377M)
7. jsonpointer-rs (106M)

**Total reach:** 1.06B downloads/month
**Combined total:** 4.9B downloads/month

### Phase 3: Parsers & Frameworks (4-8 weeks)
8. click-rs (483M)
9. jmespath-rs (405M)
10. pyparsing-rs (228M)

**Total reach:** 1.1B downloads/month
**Combined total:** 6B downloads/month

---

## Key Success Metrics

1. **Coverage**: Percentage of PyPI downloads using Rust-accelerated versions
2. **Speedup**: Geometric mean of performance improvements
3. **Adoption**: GitHub stars, PyPI downloads of Rust versions
4. **Compatibility**: Zero breaking changes from original APIs

---

## Competitive Landscape

### Existing Rust Python Projects
- **pydantic** (549M) - Already Rust-accelerated (pydantic-core)
- **cryptography** (581M) - Already uses Rust
- **orjson** - Fast JSON parsing (Rust-based)
- **polars** - DataFrame library (Rust-based)

### Our Differentiation
- Focus on pure-Python replacements
- Drop-in compatibility
- Comprehensive benchmarking
- Open ecosystem approach

---

## Resource Allocation

**Current velocity:** 2-3 packages per week (solo developer)

**Projected timeline to 6B downloads/month:** 6-8 weeks

**Bottleneck:** Testing and documentation (40% of time)

**Optimization:** Reusable testing frameworks, standardized benchmarking
