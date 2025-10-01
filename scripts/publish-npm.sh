#!/bin/bash

# NPM Publishing Script for reinvent-2025-mcp
set -e

echo "🚀 Publishing Node.js package to NPM..."

# Navigate to NPX directory
cd "$(dirname "$0")/../npx"

# Check if logged in to npm
if ! npm whoami > /dev/null 2>&1; then
    echo "❌ Not logged in to NPM. Please run: npm login"
    exit 1
fi

echo "✅ Logged in as: $(npm whoami)"

# Check if package name is available
PACKAGE_NAME=$(node -p "require('./package.json').name")
echo "📦 Checking if package name '$PACKAGE_NAME' is available..."

if npm view "$PACKAGE_NAME" > /dev/null 2>&1; then
    echo "⚠️  Package '$PACKAGE_NAME' already exists. You may need to:"
    echo "   1. Change the package name in package.json"
    echo "   2. Or increment the version if you own this package"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run tests
echo "🧪 Running tests..."
npm test

# Build/prepare package
echo "📋 Preparing package..."
npm install --production

# Publish
echo "📤 Publishing to NPM..."
npm publish

# Test installation
echo "🔍 Testing installation..."
sleep 5  # Wait for NPM to propagate
if npx "$PACKAGE_NAME" --help > /dev/null 2>&1; then
    echo "✅ Package published successfully!"
    echo "🎉 Users can now install with: npx $PACKAGE_NAME"
else
    echo "⚠️  Package published but installation test failed. May need a few minutes to propagate."
fi

echo "✨ NPM publishing complete!"
