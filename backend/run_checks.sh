#!/bin/bash

# Fast Lead - Run all health checks

set -e

echo "================================"
echo "Fast Lead - Health Checks"
echo "================================"
echo ""

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run checks
echo "Running import checks..."
python check_imports.py

echo ""
echo "Running database checks..."
python check_database.py

echo ""
echo "================================"
echo "All checks completed!"
echo "================================"
