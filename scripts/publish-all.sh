#!/bin/bash

# Master Publishing Script for reinvent-2025-mcp
set -e

echo "🚀 Publishing reinvent-2025-mcp to both NPM and PyPI..."

SCRIPT_DIR="$(dirname "$0")"

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check NPM login
if ! npm whoami > /dev/null 2>&1; then
    echo "❌ Not logged in to NPM. Please run: npm login"
    echo "   Create account at: https://www.npmjs.com/signup"
    exit 1
fi

# Check PyPI credentials
if [ ! -f ~/.pypirc ] && [ -z "$TWINE_USERNAME" ] && [ -z "$TWINE_PASSWORD" ]; then
    echo "❌ No PyPI credentials found. Please set up PyPI access:"
    echo "   1. Create account at: https://pypi.org/account/register/"
    echo "   2. Create API token at: https://pypi.org/manage/account/token/"
    echo "   3. Set environment variables:"
    echo "      export TWINE_USERNAME=__token__"
    echo "      export TWINE_PASSWORD=your-api-token"
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Publish Node.js package
echo ""
echo "📦 Publishing Node.js package..."
"$SCRIPT_DIR/publish-npm.sh"

# Publish Python package
echo ""
echo "🐍 Publishing Python package..."
"$SCRIPT_DIR/publish-pypi.sh"

echo ""
echo "🎉 All packages published successfully!"
echo ""
echo "📋 Installation commands:"
echo "   Node.js: npx reinvent-2025-mcp"
echo "   Python:  uvx reinvent-2025-mcp"
echo ""
echo "🔗 Package URLs:"
echo "   NPM: https://www.npmjs.com/package/reinvent-2025-mcp"
echo "   PyPI: https://pypi.org/project/reinvent-2025-mcp/"
