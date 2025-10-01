#!/bin/bash

# PyPI Publishing Script for reinvent-2025-mcp
set -e

echo "🐍 Publishing Python package to PyPI..."

# Navigate to UVX directory
cd "$(dirname "$0")/../uvx"

# Check if required tools are installed
if ! command -v twine &> /dev/null; then
    echo "📦 Installing build tools..."
    pip install build twine
fi

# Check if we have PyPI credentials
if [ ! -f ~/.pypirc ] && [ -z "$TWINE_USERNAME" ] && [ -z "$TWINE_PASSWORD" ]; then
    echo "❌ No PyPI credentials found. Please set up authentication:"
    echo ""
    echo "Option 1 - Environment Variables (Recommended):"
    echo "   export TWINE_USERNAME=__token__"
    echo "   export TWINE_PASSWORD=your-api-token"
    echo ""
    echo "Option 2 - Create ~/.pypirc file:"
    echo "   [pypi]"
    echo "   username = __token__"
    echo "   password = your-api-token"
    echo ""
    echo "Get API token from: https://pypi.org/manage/account/token/"
    exit 1
fi

# Get package name and check availability
PACKAGE_NAME=$(python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['name'])")
echo "📦 Checking if package name '$PACKAGE_NAME' is available..."

if pip show "$PACKAGE_NAME" > /dev/null 2>&1; then
    echo "⚠️  Package '$PACKAGE_NAME' may already exist. You may need to:"
    echo "   1. Change the package name in pyproject.toml"
    echo "   2. Or increment the version if you own this package"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run tests
echo "🧪 Running tests..."
pip install -e ".[test]"
pytest

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Build package
echo "🔨 Building package..."
python -m build

# Check package
echo "🔍 Checking package..."
twine check dist/*

# Upload to Test PyPI first (optional but recommended)
read -p "Upload to Test PyPI first for verification? (Y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "📤 Uploading to Test PyPI..."
    twine upload --repository testpypi dist/*
    
    echo "🔍 Testing installation from Test PyPI..."
    sleep 5  # Wait for propagation
    if pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ "$PACKAGE_NAME" --dry-run > /dev/null 2>&1; then
        echo "✅ Test PyPI upload successful!"
    else
        echo "⚠️  Test PyPI upload may have issues, but continuing..."
    fi
    
    read -p "Proceed with production PyPI upload? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "🛑 Stopping at Test PyPI. Check your package at: https://test.pypi.org/project/$PACKAGE_NAME/"
        exit 0
    fi
fi

# Upload to production PyPI
echo "📤 Uploading to production PyPI..."
twine upload dist/*

# Test installation
echo "🔍 Testing installation..."
sleep 10  # Wait for PyPI to propagate
if uvx "$PACKAGE_NAME" --help > /dev/null 2>&1; then
    echo "✅ Package published successfully!"
    echo "🎉 Users can now install with: uvx $PACKAGE_NAME"
else
    echo "⚠️  Package published but installation test failed. May need a few minutes to propagate."
fi

echo "✨ PyPI publishing complete!"
echo "📋 Package available at: https://pypi.org/project/$PACKAGE_NAME/"
