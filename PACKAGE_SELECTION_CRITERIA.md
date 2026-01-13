# Package Selection Criteria for Rusputyn

**Lesson Learned:** Profile packages BEFORE implementation to avoid wasted effort.

---

## ✅ Success Indicators

### 1. **CPU-Bound Operations** (Critical)

**Good:**
- String parsing/manipulation
- Encoding detection algorithms
- Regex matching
- Mathematical computations
- Data validation (regex, format checking)
- Compression/decompression
- Hashing/cryptography

**Bad:**
- Simple iteration (already optimized in Python)
- Function composition/chaining
- Code generation
- Metaprogramming

### 2. **Minimal FFI Boundary Crossings** (Critical)

**Good Pattern:**
```python
# Input once → Heavy processing → Output once
result = package.process(large_input)
```

**Bad Pattern:**
```python
# Multiple boundary crossings
for item in items:  # Each iteration crosses boundary
    result = package.process(item)  # And calls Python callback
```

### 3. **Self-Contained Algorithms** (Critical)

**Good:**
- Operates on data structures (strings, bytes, numbers)
- No Python callbacks/predicates
- Returns simple types (bool, str, int, dict)

**Bad:**
- Requires Python functions as arguments
- Calls user-provided callbacks
- Returns complex nested iterators
- Needs Python's type system

### 4. **Large Input / Output Ratio** (Important)

**Good:**
```python
# Process 1MB of data → return 100 bytes
encoding = detect_encoding(large_file_bytes)

# Parse 10KB string → return structured data
config = parse_toml(file_content)
```

**Bad:**
```python
# Process 100 items → return 100 items (1:1)
chunks = chunked(items, 10)

# Minimal processing per item
first_item = first(iterable)
```

### 5. **Hot Path Operations** (Important)

**Good:**
- Called in tight loops
- Part of critical paths
- Used in data processing pipelines

**Bad:**
- Called once per application run
- Initialization code
- Configuration loading (unless parsing is complex)

---

## 🔬 Pre-Implementation Profiling Checklist

Before implementing a package, answer these questions:

### A. Package Characteristics

- [ ] **Download volume:** >100M/month?
- [ ] **Pure Python:** No C extensions?
- [ ] **Stable API:** Not rapidly changing?

### B. Performance Profile

- [ ] **CPU-intensive:** Does it do significant computation?
- [ ] **Boundary crossings:** Can it process data in bulk?
- [ ] **No callbacks:** Doesn't require Python functions?
- [ ] **Return simple types:** Bool, str, int, dict, list of primitives?

### C. Quick Test (30 minutes)

1. **Create minimal POC:**
   ```rust
   #[pyfunction]
   fn test_function(input: &str) -> PyResult<String> {
       // Minimal implementation
   }
   ```

2. **Benchmark against Python:**
   ```python
   # If Rust is slower or <5x faster → STOP
   ```

3. **Decision:**
   - **>10x faster:** ✅ Proceed
   - **5-10x faster:** ⚠️ Consider (may need optimization)
   - **<5x faster:** ❌ Abandon

---

## 📊 Package Evaluation Matrix

### Tier 1: Excellent Candidates (>10x expected)

| Package | CPU-Bound | Few Boundaries | No Callbacks | Simple Returns | Score |
|---------|-----------|----------------|--------------|----------------|-------|
| **pyparsing** | ✅ Heavy | ✅ Bulk text | ✅ Grammar-based | ✅ AST | 4/4 |
| **charset-normalizer** | ✅ Heavy | ✅ File bytes | ✅ Algorithm | ✅ String | 4/4 |
| **validators** | ✅ Regex | ✅ Per-string | ✅ Built-in | ✅ Bool | 4/4 |
| **python-dotenv** | ✅ Parsing | ✅ File content | ✅ No callbacks | ✅ Dict | 4/4 |
| **dateutil** | ✅ Parsing | ✅ Per-string | ✅ Built-in | ✅ Datetime | 4/4 |

### Tier 2: Moderate Candidates (5-10x expected)

| Package | CPU-Bound | Few Boundaries | No Callbacks | Simple Returns | Score |
|---------|-----------|----------------|--------------|----------------|-------|
| **tomli** | ✅ Parsing | ✅ File content | ✅ No callbacks | ⚠️ Nested dict | 3/4 |
| **humanize** | ✅ Format logic | ✅ Per-value | ✅ Built-in | ✅ String | 4/4 |
| **tabulate** | ⚠️ Formatting | ⚠️ Per-row | ✅ Built-in | ✅ String | 3/4 |
| **packaging** | ✅ Version parse | ✅ Per-string | ✅ Built-in | ✅ Object | 4/4 |

### Tier 3: Poor Candidates (<5x expected)

| Package | CPU-Bound | Few Boundaries | No Callbacks | Simple Returns | Score |
|---------|-----------|----------------|--------------|----------------|-------|
| **more-itertools** | ❌ Iteration | ❌ Per-item | ❌ User funcs | ❌ Iterators | 0/4 |
| **attrs** | ❌ Codegen | ❌ Class def | ❌ Python AST | ❌ Methods | 0/4 |
| **click** | ❌ Decorators | ❌ Many calls | ❌ User funcs | ❌ CLI state | 0/4 |

---

## 🎯 Decision Tree

```
Start
  ↓
Is it CPU-bound?
  ├─ No → ❌ REJECT
  ↓
  Yes
  ↓
Does it call Python functions?
  ├─ Yes → ❌ REJECT (or flag for careful review)
  ↓
  No
  ↓
Can it process data in bulk?
  ├─ No → ❌ REJECT (too many boundary crossings)
  ↓
  Yes
  ↓
Create 30-min POC
  ↓
Benchmark
  ↓
Speedup?
  ├─ <5x → ❌ REJECT
  ├─ 5-10x → ⚠️ REVIEW (estimate effort vs. gain)
  └─ >10x → ✅ PROCEED
```

---

## 📝 Real Examples

### ✅ SUCCESS: charset-normalizer-rs

**Profile:**
- **Input:** 1MB file bytes
- **Processing:** Complex encoding detection algorithms
- **Output:** String (encoding name)
- **Boundary crossings:** 2 (input + output)
- **CPU work:** Thousands of operations per byte

**Result:** 261x faster ✅

---

### ❌ FAILURE: more-itertools-rs

**Profile:**
- **Input:** Python iterable (lazy)
- **Processing:** Simple iteration logic
- **Output:** Python iterable (lazy)
- **Boundary crossings:** N (every item)
- **Callbacks:** Yes (predicates, key functions)
- **CPU work:** Minimal per item

**Result:** 0.5-1.3x (SLOWER in many cases) ❌

---

### ⚠️ MARGINAL: colorama-rs

**Profile:**
- **Input:** None (ANSI codes)
- **Processing:** String constants
- **Output:** String
- **Boundary crossings:** Many (per color call)
- **CPU work:** Nearly zero

**Result:** 1.2-1.3x (works, but barely worth it) ⚠️

---

## 🔍 Quick Profiling Script

Use this to evaluate packages:

```python
#!/usr/bin/env python3
"""Quick package profiler for Rusputyn candidates"""

import time
import cProfile
import pstats
from io import StringIO

def profile_package(package_name, test_function):
    """Profile a package's hot path"""

    profiler = cProfile.Profile()
    profiler.enable()

    # Run test workload
    start = time.perf_counter()
    for _ in range(10000):
        test_function()
    end = time.perf_counter()

    profiler.disable()

    # Analyze
    s = StringIO()
    stats = pstats.Stats(profiler, stream=s)
    stats.sort_stats('cumulative')
    stats.print_stats(20)

    print(f"\n{package_name} Profile:")
    print(f"Total time: {(end-start)*1000:.2f}ms")
    print(f"Per-call: {(end-start)*100:.2f}µs")
    print("\nTop functions:")
    print(s.getvalue()[:1000])

    # Decision helpers
    print("\n" + "="*60)
    print("DECISION CRITERIA:")
    print("="*60)

    # Check for Python function calls
    if "call_function" in s.getvalue() or "PyObject_Call" in s.getvalue():
        print("⚠️  Contains Python function calls - may be problematic")

    # Check for heavy computation
    if end - start > 0.5:  # >500ms for 10k calls
        print("✅ CPU-intensive enough for Rust")
    else:
        print("❌ Too fast - FFI overhead will dominate")

# Example usage:
# import more_itertools as mit
# profile_package("more-itertools", lambda: list(mit.chunked(range(100), 10)))
```

---

## 🎓 Lessons Learned

### From more-itertools-rs:
1. ❌ Simple iteration is already optimized in Python
2. ❌ Lazy iterators don't translate well to Rust
3. ❌ Python callbacks from Rust are extremely slow
4. ❌ Many small boundary crossings kill performance

### From attrs analysis:
1. ❌ Metaprogramming/code generation happens once (not hot path)
2. ❌ Python-specific features (AST, metaclasses) can't be accelerated
3. ❌ Zero runtime overhead = nothing to optimize

### From successful packages:
1. ✅ Heavy algorithms benefit massively
2. ✅ Bulk processing amortizes FFI cost
3. ✅ Simple in/out with complex middle = perfect
4. ✅ No Python callbacks = clean boundary

---

## 🚀 Recommended Next Targets

Based on criteria:

### 1. pyparsing (228M downloads)
- ✅ Heavy parsing algorithms
- ✅ Bulk text processing
- ✅ Grammar-based (no callbacks)
- ✅ Returns AST
- **Expected:** 20-50x

### 2. pytz (377M downloads)
- ✅ Timezone calculations
- ✅ Bulk lookups possible
- ✅ Data-driven (no callbacks)
- ✅ Returns datetime
- **Expected:** 10-25x

### 3. jsonpointer (106M downloads)
- ✅ Path parsing/evaluation
- ✅ JSON navigation
- ✅ No callbacks
- ✅ Returns value
- **Expected:** 15-30x

---

## 📋 Pre-Implementation Template

For each new package, fill this out:

```markdown
# Package: [name]
## Downloads: [X]M/month

### Profiling Results
- [ ] CPU-bound: [Yes/No + evidence]
- [ ] Boundary crossings: [Few/Many + count]
- [ ] Python callbacks: [None/Some + impact]
- [ ] Return types: [Simple/Complex]

### 30-Minute POC
- Implementation time: [X] minutes
- Benchmark result: [X]x faster
- Decision: [Proceed/Review/Reject]

### Risk Assessment
- FFI overhead: [Low/Medium/High]
- Implementation complexity: [Low/Medium/High]
- Maintenance burden: [Low/Medium/High]

### GO/NO-GO Decision
[Proceed/Reject] - [reasoning]
```

---

## 🎯 Success Metrics

A package is worth implementing if:

1. **Minimum 10x speedup** on typical workloads
2. **Maximum 4 weeks** implementation time
3. **High confidence** in achieving target speedup
4. **Clear value proposition** for users

If any criterion fails → Document why and move on.

---

*This framework prevents wasted effort on packages that can't achieve Rusputyn's 10x+ performance standard.*
