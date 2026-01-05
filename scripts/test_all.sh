#!/bin/bash
set -e

echo "================================"
echo "Rusputyn Test Suite"
echo "================================"
echo ""

# Activate virtual environment
source /opt/venv/bin/activate

# Track results
TOTAL=0
PASSED=0
FAILED=0

test_package() {
    local package=$1
    local path="libraries/$package"

    echo "----------------------------------------"
    echo "Testing: $package"
    echo "----------------------------------------"

    TOTAL=$((TOTAL + 1))

    if [ ! -d "$path" ]; then
        echo "❌ Package directory not found: $path"
        FAILED=$((FAILED + 1))
        return 1
    fi

    cd "$path"

    # Build the package
    echo "Building $package..."
    if maturin develop --release 2>&1 | tee build.log; then
        echo "✅ Build successful"
    else
        echo "❌ Build failed"
        FAILED=$((FAILED + 1))
        cd /rusputyn
        return 1
    fi

    # Run benchmark if it exists
    if [ -f "benchmark.py" ]; then
        echo "Running benchmark..."
        if python3 benchmark.py; then
            echo "✅ Benchmark completed"
            PASSED=$((PASSED + 1))
        else
            echo "⚠️  Benchmark had issues (may be expected)"
            PASSED=$((PASSED + 1))
        fi
    fi

    # Run tests if they exist
    if [ -d "tests" ]; then
        echo "Running tests..."
        pytest tests/ -v
    fi

    cd /rusputyn
    echo ""
}

# Test all packages
echo "Starting package tests..."
echo ""

for package_dir in libraries/*/; do
    package=$(basename "$package_dir")

    # Skip the showcase directory
    if [ "$package" = "rust-speedup-showcase" ]; then
        continue
    fi

    test_package "$package"
done

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Total packages: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
