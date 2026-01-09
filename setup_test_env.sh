#!/bin/bash
# Setup test environment for character-skill-trees

echo "Setting up test environment for character-skill-trees..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "Installing character-skill-trees in development mode..."
pip install -e .

# Install test dependencies
echo "Installing test dependencies..."
pip install -r requirements-test.txt

echo ""
echo "✓ Test environment setup complete!"
echo ""
echo "To run tests:"
echo "  source venv/bin/activate"
echo "  pytest tests/ -v"
echo ""
echo "Or use the test runner:"
echo "  python tests/run_tests.py --help"
