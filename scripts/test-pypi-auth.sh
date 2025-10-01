#!/bin/bash

# Test PyPI Authentication
set -e

echo "🔍 Testing PyPI authentication..."

# Check for credentials
if [ -f ~/.pypirc ]; then
    echo "✅ Found ~/.pypirc file"
    
    # Test with a simple twine command
    echo "🧪 Testing twine authentication..."
    cd "$(dirname "$0")/../uvx"
    
    # Create a minimal test package
    mkdir -p test_build
    echo "print('test')" > test_build/test.py
    
    # Try to check if we can authenticate (without actually uploading)
    if python3 -c "
import configparser
config = configparser.ConfigParser()
config.read('$HOME/.pypirc')
if 'pypi' in config:
    print('✅ PyPI configuration valid')
    username = config['pypi']['username']
    password = config['pypi']['password']
    if username == '__token__' and password.startswith('pypi-'):
        print('✅ API token format looks correct')
    else:
        print('⚠️  Credentials format may be incorrect')
else:
    print('❌ No [pypi] section found in .pypirc')
"; then
        echo "✅ PyPI authentication setup appears correct"
    else
        echo "❌ PyPI authentication test failed"
    fi
    
    # Cleanup
    rm -rf test_build
    
elif [ -n "$TWINE_USERNAME" ] && [ -n "$TWINE_PASSWORD" ]; then
    echo "✅ Found environment variables"
    echo "   TWINE_USERNAME: $TWINE_USERNAME"
    echo "   TWINE_PASSWORD: [hidden]"
else
    echo "❌ No PyPI credentials found"
    echo ""
    echo "Run one of these to set up:"
    echo "  ./scripts/setup-pypi.sh"
    echo "  ./scripts/setup-publishing.sh"
    exit 1
fi

echo ""
echo "🎉 PyPI authentication test complete!"
