# AWS re:Invent 2025 MCP Server (Python)

Python implementation of the MCP server for AWS re:Invent 2025 session catalog with 1,843 sessions.

## Features

- **13 MCP Tools** for comprehensive session discovery
- **MessagePack data format** for 30% faster loading and smaller size
- **Simple array-based architecture** for minimal complexity
- **Pagination support** for all search and filter operations

## Quick Start

### Install Dependencies
```bash
pip install -e .
```

### Run Server
```bash
python3 src/reinvent_2025_mcp/main.py
```

### Test with MCP Inspector
```bash
npx @modelcontextprotocol/inspector python3 src/reinvent_2025_mcp/main.py
```

## Available Tools

1. **search_sessions** - Fuzzy search across all session content
2. **search_services** - Find AWS services by name/abbreviation  
3. **get_session_details** - Get complete session information
4. **list_categories** - Browse available category values
5. **get_sessions_by_service** - Find sessions for specific AWS service
6. **get_sessions_by_level** - Filter sessions by difficulty level
7. **get_sessions_by_role** - Find sessions for specific job functions
8. **get_sessions_by_industry** - Find sessions for industry verticals
9. **get_sessions_by_segment** - Find sessions for business segments
10. **get_sessions_by_feature** - Find sessions by format/feature type
11. **get_sessions_by_topic** - Find sessions by technical domain
12. **get_sessions_by_area_of_interest** - Find sessions by interest areas
13. **search_speakers** - Search speakers by name or get all speakers with their sessions

## Architecture

- **Data Layer**: MessagePack loading into memory array
- **Service Layer**: Array filtering and search operations  
- **MCP Layer**: Tool registration and request handling
- **Utilities**: Simple string matching and pagination

## Performance

- **Startup**: <1 second for 1,843 sessions
- **Memory**: ~30MB total footprint
- **Search**: <10ms response times for typical queries
- **Data Size**: 2.3MB MessagePack vs 3.1MB JSON (25% smaller)

## Dependencies

- `mcp>=1.15.0`: MCP protocol implementation
- `msgpack>=1.1.0`: Fast binary serialization

## Testing

Core functionality verified:
- ✅ Data loading (1,843 sessions from MessagePack)
- ✅ Search operations (294 sessions found for "bedrock")
- ✅ Session filtering and pagination
- ✅ All 13 tools initialized correctly
