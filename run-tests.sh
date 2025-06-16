#!/bin/bash

# A script to run the full test suite with a nice summary.
# This script uses gotestsum for better test output.

# Check if gotestsum is installed
if ! command -v gotestsum &>/dev/null; then
    echo "gotestsum could not be found. To install it, run:"
    echo "go install gotest.tools/gotestsum@latest"
    exit 1
fi

# Default command
gotestsum_args=("--format" "standard-verbose")
go_test_args=("-v" "./...")

# Check for coverage flag
if [[ " $* " == *" --coverage "* ]]; then
    echo "Running tests with coverage enabled..."
    go_test_args+=("-coverprofile=coverage.out" "-covermode=atomic")
else
    echo "Running tests..."
fi

gotestsum "${gotestsum_args[@]}" -- "${go_test_args[@]}"

# Check if coverage was generated and if html report is requested
if [[ -f "coverage.out" && " $* " == *" --html "* ]]; then
    echo "Opening HTML coverage report..."
    go tool cover -html=coverage.out
fi
