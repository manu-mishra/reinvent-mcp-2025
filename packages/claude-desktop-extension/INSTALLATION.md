# Installation Guide - re:Invent 2025 Claude Desktop Extension

## Quick Start

### Option 1: Python Version (Recommended)
1. Download `reinvent-2025-session-catalog-python.dxt`
2. Open Claude Desktop
3. Navigate to Extensions tab
4. Drag and drop the `.dxt` file into the Extensions window
5. Click "Install"
6. The extension will automatically install the Python package via `uvx`

### Option 2: Node.js Version
1. Download `reinvent-2025-session-catalog-nodejs.dxt`
2. Follow the same installation steps as above
3. The extension will automatically install the Node.js package via `npx`

## System Requirements

### Python Version
- **Python**: 3.11 or higher
- **Package Manager**: uvx (automatically installed if needed)
- **Platform**: Windows, macOS, Linux

### Node.js Version
- **Node.js**: 18 or higher
- **Package Manager**: npm/npx (comes with Node.js)
- **Platform**: Windows, macOS, Linux

## Verification

After installation, test the extension by asking Claude:

```
"Find all AI sessions at re:Invent 2025"
```

You should see Claude access the session catalog and return relevant results.

## Usage Examples

### Basic Search
- "Show me all sessions about serverless computing"
- "Find sessions for beginners (level 100)"
- "What sessions are available for data engineers?"

### Advanced Filtering
- "Find hands-on workshops about machine learning"
- "Show me sessions for the healthcare industry"
- "List all sessions by AWS speakers about security"

### Speaker Discovery
- "Who is speaking about generative AI?"
- "Find all sessions by speakers from Amazon"
- "Show me the session details for AIM236-S"

## Troubleshooting

### Installation Issues
- **Permission Errors**: Ensure Claude Desktop has necessary permissions
- **Network Issues**: Check internet connection for package downloads
- **Package Manager**: Ensure uvx (Python) or npx (Node.js) is available

### Runtime Issues
- **Command Not Found**: Restart Claude Desktop after installation
- **Slow Responses**: First query may be slower due to data loading
- **No Results**: Verify the extension is enabled in Claude Desktop settings

## Uninstallation

1. Open Claude Desktop
2. Go to Extensions
3. Find "re:Invent 2025 Session Catalog"
4. Click "Remove" or "Uninstall"

## Support

For issues or questions:
- **GitHub Issues**: https://github.com/manu-mishra/reinvent-mcp-2025/issues
- **Documentation**: https://github.com/manu-mishra/reinvent-mcp-2025
- **MCP Protocol**: https://modelcontextprotocol.io/

## What's Included

The extension provides access to:
- **1,843 Sessions** from AWS re:Invent 2025
- **13 MCP Tools** for session discovery and filtering
- **Complete Speaker Database** with session mappings
- **Rich Metadata** including levels, topics, industries, and more
