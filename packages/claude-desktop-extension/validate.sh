#!/bin/bash

# Validation script for re:Invent 2025 Claude Desktop Extensions (.mcpb)

set -e

echo "🔍 Validating Claude Desktop Extensions..."

validate_package() {
    local package_file=$1
    echo "📋 Validating $package_file..."
    
    # Check if file exists
    if [ ! -f "$package_file" ]; then
        echo "❌ File $package_file not found"
        return 1
    fi
    
    # Check if it's a valid zip file
    if ! unzip -t "$package_file" > /dev/null 2>&1; then
        echo "❌ $package_file is not a valid zip file"
        return 1
    fi
    
    # Check required files
    local temp_dir=$(mktemp -d)
    unzip -q "$package_file" -d "$temp_dir"
    
    # Check manifest.json exists
    if [ ! -f "$temp_dir/manifest.json" ]; then
        echo "❌ manifest.json missing in $package_file"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Validate JSON syntax
    if ! python3 -m json.tool "$temp_dir/manifest.json" > /dev/null 2>&1; then
        echo "❌ Invalid JSON in manifest.json for $package_file"
        rm -rf "$temp_dir"
        return 1
    fi
    
    # Check required manifest fields
    local required_fields=("name" "version" "description" "server")
    for field in "${required_fields[@]}"; do
        if ! grep -q "\"$field\"" "$temp_dir/manifest.json"; then
            echo "❌ Missing required field '$field' in manifest.json for $package_file"
            rm -rf "$temp_dir"
            return 1
        fi
    done
    
    echo "✅ $package_file is valid"
    rm -rf "$temp_dir"
    return 0
}

validate_package "reinvent-2025-session-catalog-python.mcpb"
validate_package "reinvent-2025-session-catalog-nodejs.mcpb"

echo ""
echo "🎉 All packages are valid!"
echo "📦 Ready for distribution and installation in Claude Desktop"
