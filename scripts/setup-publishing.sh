#!/bin/bash

# Setup Script for First-Time Publishing
set -e

echo "🔧 Setting up publishing environment for reinvent-2025-mcp..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Node.js and npm
if ! command_exists node; then
    echo "❌ Node.js not found. Please install from: https://nodejs.org/"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm not found. Please install Node.js from: https://nodejs.org/"
    exit 1
fi

# Check Python and pip
if ! command_exists python3; then
    echo "❌ Python 3 not found. Please install from: https://python.org/"
    exit 1
fi

if ! command_exists pip; then
    echo "❌ pip not found. Please install Python from: https://python.org/"
    exit 1
fi

echo "✅ Node.js $(node --version) and Python $(python3 --version) found"

# Install Python publishing tools
echo "📦 Installing Python publishing tools..."
pip install build twine

# Check uvx
if ! command_exists uvx; then
    echo "📦 Installing uvx..."
    pip install uvx
fi

echo "✅ Publishing tools installed"

# NPM Login Check
echo ""
echo "🔐 Checking NPM authentication..."
if npm whoami > /dev/null 2>&1; then
    echo "✅ Already logged in to NPM as: $(npm whoami)"
else
    echo "❌ Not logged in to NPM"
    echo ""
    echo "📋 To set up NPM publishing:"
    echo "   1. Create account at: https://www.npmjs.com/signup"
    echo "   2. Verify your email"
    echo "   3. Run: npm login"
    echo "   4. Enter your credentials"
    echo ""
    read -p "Do you want to login to NPM now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npm login
    fi
fi

# PyPI Setup Check
echo ""
echo "🔐 Checking PyPI authentication..."
if [ -f ~/.pypirc ]; then
    echo "✅ PyPI credentials found in ~/.pypirc"
elif [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ]; then
    echo "✅ PyPI credentials found in environment variables"
else
    echo "❌ No PyPI credentials found"
    echo ""
    read -p "Do you want to set up PyPI credentials now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        "$(dirname "$0")/setup-pypi.sh"
    else
        echo "💡 Run './scripts/setup-pypi.sh' later to configure PyPI"
    fi
fi

# Make scripts executable
echo ""
echo "🔧 Making scripts executable..."
chmod +x "$(dirname "$0")/publish-npm.sh"
chmod +x "$(dirname "$0")/publish-pypi.sh"
chmod +x "$(dirname "$0")/publish-all.sh"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Review package names in package.json and pyproject.toml"
echo "   2. Update version numbers if needed"
echo "   3. Run: ./scripts/publish-all.sh"
echo ""
echo "🔗 Account creation links:"
echo "   NPM: https://www.npmjs.com/signup"
echo "   PyPI: https://pypi.org/account/register/"
