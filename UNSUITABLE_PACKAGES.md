# Unsuitable Packages for Rusputyn

Packages evaluated and rejected due to fundamental incompatibility with Rust optimization.

---

## ❌ attrs (443M downloads/month)

**Reason:** Metaprogramming - code generation at class definition time
- Not CPU-bound (happens once per class)
- Requires Python AST/metaclass system
- Zero runtime overhead already
- **Expected speedup:** 1-2x

---

## ❌ more-itertools (171M downloads/month)

**Reason:** FFI overhead exceeds gains
- Simple iteration already optimized in Python
- Requires Python callbacks (predicates)
- Many small boundary crossings per item
- **Measured speedup:** 0.7x (SLOWER)
- **Status:** Implemented, benchmarked, abandoned

---

## ❌ pyparsing (228M downloads/month)

**Reason:** Parser combinator design incompatible
- Dynamic grammar composition at runtime
- Requires Python callbacks everywhere
- Already fast (9.2µs per parse)
- **Expected speedup:** 0.5-2x
- **Status:** Quick benchmark, rejected

---

## Pattern: Why These Fail

1. **Python callbacks from Rust** - 100x overhead
2. **Already fast operations** - <10µs leaves no room
3. **Metaprogramming** - Python-specific features
4. **Dynamic composition** - Can't pre-compile

---

## Better Alternatives to Explore

- pytz (377M) - timezone calculations
- jsonpointer (106M) - JSON path operations
- Others from existing successful pattern
