#!/bin/bash

# Build script for re:Invent 2025 Claude Desktop Extension (.mcpb format)

set -e

echo "🚀 Building re:Invent 2025 Claude Desktop Extension (.mcpb format)..."

# Function to build an MCPB package
build_mcpb() {
    local version=$1
    local manifest_file=$2
    local output_file=$3
    
    echo "📦 Building $version version..."
    
    # Create build directory
    BUILD_DIR="build-$version"
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"
    
    # Copy files
    cp "$manifest_file" "$BUILD_DIR/manifest.json"
    cp README.md "$BUILD_DIR/"
    
    # Create a simple icon placeholder if it doesn't exist
    if [ ! -f "icon.png" ]; then
        echo "Creating placeholder icon for $version..."
        # Create a 1x1 transparent PNG as placeholder
        echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" | base64 -d > "$BUILD_DIR/icon.png"
    else
        cp icon.png "$BUILD_DIR/"
    fi
    
    # Create the .mcpb file (zip format)
    cd "$BUILD_DIR"
    zip -r "../$output_file" . > /dev/null
    cd ..
    
    echo "✅ Built $output_file successfully!"
    
    # Clean up build directory
    rm -rf "$BUILD_DIR"
}

# Build Node.js version  
build_mcpb "Node.js" "manifest-nodejs.json" "reinvent-2025-session-catalog-nodejs.mcpb"

# Copy to claude folder in root
echo "📋 Copying to claude folder..."
mkdir -p ../../claude
cp reinvent-2025-session-catalog-nodejs.mcpb ../../claude/

echo ""
echo "🎉 Extension built successfully!"
echo "📋 Available files:"
echo "   • packages/claude-desktop-extension/reinvent-2025-session-catalog-nodejs.mcpb"
echo "   • claude/reinvent-2025-session-catalog-nodejs.mcpb"
echo ""
echo "📖 Installation:"
echo "   1. Open Claude Desktop"
echo "   2. Go to Extensions"
echo "   3. Drag and drop the .mcpb file"
echo "   4. Click Install"
