# re:Invent 2025 MCP Server - Packages

This directory contains packaging configurations for different platforms and distribution methods.

## Available Packages

### Claude Desktop Extensions (.mcpb)

**Location**: `claude-desktop-extension/`

One-click installation package for Claude Desktop that eliminates the need for manual JSON configuration.

**Available Version**:
- `reinvent-2025-session-catalog-nodejs.mcpb` - Node.js/npx version

**Build Instructions**:
```bash
cd claude-desktop-extension
./build.sh
```

**Installation**:
1. Open Claude Desktop
2. Navigate to Extensions
3. Drag and drop the `.mcpb` file
4. Click "Install"

### Features

- **One-click Installation**: No manual configuration required
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Automatic Dependencies**: Handles package installation automatically
- **Secure**: Sandboxed execution environment

## Future Packages

Additional packaging formats planned:
- **VS Code Extension**: For GitHub Copilot and other VS Code MCP integrations
- **Cursor IDE Package**: Native Cursor IDE integration
- **Continue.dev Plugin**: Plugin format for Continue.dev
- **Standalone Executables**: Self-contained binaries for air-gapped environments

## Development

To add new packaging formats:

1. Create a new subdirectory under `packages/`
2. Add appropriate manifest/configuration files
3. Create build scripts
4. Update this README

## Requirements

- **Node.js Version**: Node.js 18+ with npx
- **Build Tools**: zip utility for .mcpb packaging

## Support

For packaging issues or requests for new formats, please open an issue at:
https://github.com/manu-mishra/reinvent-mcp-2025/issues
