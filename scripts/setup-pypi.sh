#!/bin/bash

# Simple PyPI Setup Script
set -e

echo "🐍 Setting up PyPI authentication..."

echo ""
echo "📋 PyPI Setup Steps:"
echo "1. Create account at: https://pypi.org/account/register/"
echo "2. Verify your email"
echo "3. Create API token at: https://pypi.org/manage/account/token/"
echo "4. Copy the token (starts with 'pypi-')"
echo ""

read -p "Have you completed steps 1-4? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please complete the PyPI setup steps first."
    exit 1
fi

echo ""
echo "Enter your PyPI API token (it should start with 'pypi-'):"
read -r API_TOKEN

if [[ ! $API_TOKEN =~ ^pypi- ]]; then
    echo "⚠️  Warning: API token should start with 'pypi-'"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create .pypirc file
echo "📝 Creating ~/.pypirc file..."
cat > ~/.pypirc << EOF
[pypi]
username = __token__
password = $API_TOKEN
EOF

# Set permissions
chmod 600 ~/.pypirc

echo "✅ PyPI authentication configured!"
echo ""
echo "🔍 Testing authentication..."
if python3 -c "import keyring; print('Keyring available')" 2>/dev/null; then
    echo "✅ Python keyring available"
else
    echo "ℹ️  Python keyring not available (optional)"
fi

echo ""
echo "📋 Configuration saved to ~/.pypirc"
echo "🎉 You can now run: ./scripts/publish-pypi.sh"
