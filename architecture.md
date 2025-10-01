# MCP Server Architecture for AWS re:Invent 2025

## Overview

This document defines the architecture for both Python and Node.js MCP server implementations. The architecture uses a simplified array-based data model with in-memory data loading and minimal third-party dependencies.

## Simplified Data Model

### Direct Array Approach
- **sessions**: Array of session objects with embedded metadata
- **No normalization**: All session data stored directly in session objects
- **No bridge tables**: Many-to-many relationships stored as arrays within sessions

### Session Object Structure
```javascript
{
  code: "DVT222-S",
  title: "Session Title",
  abstract: "Session description...",
  speakers: [
    {
      fullName: "John Doe",
      jobTitle: "Senior Engineer", 
      companyName: "AWS",
      roles: "Speaker"
    }
  ],
  attributes: {
    topics: ["Artificial Intelligence", "Machine Learning"],
    services: ["Amazon Bedrock", "Amazon SageMaker"],
    industries: ["Financial Services", "Healthcare"],
    roles: ["Developer / Engineer", "Data Scientist"],
    level: ["300 – Advanced"],
    segments: ["Enterprise", "Developer Community"],
    areas_of_interest: ["Generative AI", "Machine Learning"],
    features: ["Interactive", "Hands-on"]
  },
  type: "Breakout Session",
  // ... other session metadata
}
```

## Architecture Components

### 1. Data Layer
- **Purpose**: Load MessagePack data into memory as array
- **Implementation**: Direct array of session objects
- **Loading**: MessagePack data loaded directly at startup
- **Size**: 2.3MB MessagePack file with 1,843 sessions

### 2. Service Layer
- **Purpose**: Business logic for session discovery, filtering, and speaker search
- **Implementation**: Array filtering and search operations
- **Key Methods**:
  - `search_sessions()` - Search sessions or list all (empty query)
  - `search_speakers()` - Search speakers or list all (empty query, 5 per page)
  - Filter methods for categories, levels, roles, etc.
- **Responsibilities**: Filter, search, paginate session array, extract speaker data

### 3. MCP Layer
- **Purpose**: MCP protocol implementation and tool registration
- **Implementation**: Framework-specific MCP server setup
- **Tools**: 13 MCP tools with comprehensive session and speaker discovery
- **Responsibilities**: Tool definitions, request handling, response formatting

## Key Features

### Empty Query Behavior
- **`search_sessions`**: Empty string returns all 1,843 sessions
- **`search_speakers`**: Empty string returns all speakers (5 per page)
- **Purpose**: Allows tools to function as both search and list operations

### Speaker Discovery
- **Data Extraction**: Speakers extracted from session objects into deduplicated list
- **Response Format**: Speaker details with nested sessions array
- **Pagination**: 5 speakers per page (configurable)
- **Session Nesting**: Each speaker includes array of their sessions (code + title)

### 4. Utility Layer
- **Purpose**: Common utilities and helpers
- **Implementation**: Simple string matching and pagination functions
- **Responsibilities**: Fuzzy matching, cursor handling, array operations

## File Structure

### Python Implementation (`uvx/`)

```
uvx/
├── pyproject.toml                 # Package configuration
├── src/
│   └── reinvent_2025_mcp/
│       ├── __init__.py           # Package initialization
│       ├── main.py               # Entry point and MCP server setup
│       ├── data/
│       │   ├── __init__.py
│       │   ├── loader.py         # MessagePack data loading
│       │   └── sessions.msgpack  # Bundled session data (MessagePack format)
│       ├── services/
│       │   ├── __init__.py
│       │   └── session_service.py # All session operations (search, filter, details)
│       ├── tools/
│       │   ├── __init__.py
│       │   └── session_tools.py  # All MCP tools
│       └── utils/
│           ├── __init__.py
│           ├── search.py         # Simple string matching
│           └── pagination.py     # Cursor-based pagination
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py       # Data loading tests
│   ├── test_services.py          # Service layer tests
│   ├── test_tools.py             # MCP tool tests
│   └── test_utils.py             # Utility function tests
└── README.md                     # Python-specific documentation
```

### Node.js Implementation (`npx/`)

```
npx/
├── package.json                  # Package configuration
├── src/
│   ├── index.js                  # Entry point and MCP server setup
│   ├── data/
│   │   ├── loader.js             # MessagePack data loading
│   │   └── sessions.msgpack      # Bundled session data (MessagePack format)
│   ├── services/
│   │   └── sessionService.js     # All session operations (search, filter, details)
│   ├── tools/
│   │   └── sessionTools.js       # All MCP tools
│   └── utils/
│       ├── search.js             # Simple string matching
│       └── pagination.js         # Cursor-based pagination
├── tests/
│   ├── dataLoader.test.js        # Data loading tests
│   ├── services.test.js          # Service layer tests
│   ├── tools.test.js             # MCP tool tests
│   └── utils.test.js             # Utility function tests
└── README.md                     # Node.js-specific documentation
```

## Dependencies

### Python Dependencies
```toml
[project]
dependencies = [
    "mcp>=1.15.0",           # MCP protocol implementation
    "msgpack>=1.1.0",        # Fast binary serialization
]
```

### Node.js Dependencies
```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.18.2",
    "@msgpack/msgpack": "^3.1.2"
  }
}
```

## Data Format Optimization

### Format Comparison

| Format | Load Speed | File Size | Compatibility | Dependencies |
|--------|------------|-----------|---------------|--------------|
| **JSON** | Fast | Large | Universal | None |
| **MessagePack** | Faster | 30% smaller | Good | msgpack library |
| **CBOR** | Similar to JSON | 27% smaller | Good | cbor2 library |
| **BSON** | Slower serialize, faster deserialize | Larger | Limited | bson library |

### Recommended Approach: **MessagePack**

**Rationale:**
- **30-50% faster loading** than JSON in most benchmarks
- **30% smaller file size** reduces package size and memory usage
- **Excellent cross-language support** (Python: `msgpack`, Node.js: `msgpack`)
- **Minimal dependency overhead** - single lightweight library

### Implementation Strategy

#### Data Preparation (Build Time)
```bash
# Convert JSON to MessagePack during build
python scripts/convert_data.py data/sessions.json → data/sessions.msgpack
```

#### Runtime Loading (Both Languages)
```python
# Python
import msgpack
with open('data/sessions.msgpack', 'rb') as f:
    data = msgpack.unpack(f, raw=False)
```

```javascript
// Node.js  
const msgpack = require('msgpack');
const fs = require('fs');
const data = msgpack.decode(fs.readFileSync('data/sessions.msgpack'));
```

### Updated Dependencies

#### Python Dependencies
```toml
[project]
dependencies = [
    "mcp>=1.15.0",           # MCP protocol implementation
    "msgpack>=1.1.0",        # Fast binary serialization (actively maintained)
    "pytest>=8.0.0",        # Testing framework
    "pytest-asyncio>=0.23.0" # Async testing support
]
```

#### Node.js Dependencies
```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.18.2",
    "@msgpack/msgpack": "^3.1.2",
    "jest": "^29.7.0"
  }
}
```

### Cross-Platform Compatibility

**✅ Fully Compatible**: MessagePack data written by Python can be read by Node.js and vice versa

#### Runtime Loading Examples

**Python Implementation:**
```python
import msgpack

# Load MessagePack data
with open('data/sessions.msgpack', 'rb') as f:
    data = msgpack.unpack(f, raw=False, strict_map_key=False)
```

**Node.js Implementation:**
```javascript
import { decode } from '@msgpack/msgpack';
import { readFileSync } from 'fs';

// Load MessagePack data  
const buffer = readFileSync('data/sessions.msgpack');
const data = decode(buffer);
```

### Data Conversion Script

Create identical MessagePack files for both platforms:

```python
# scripts/convert_to_msgpack.py
import json
import msgpack

# Load original JSON
with open('data/sessions.json', 'r') as f:
    data = json.load(f)

# Save as MessagePack (compatible with both Python and Node.js)
with open('data/sessions.msgpack', 'wb') as f:
    msgpack.pack(data, f, use_bin_type=True)

### Performance Benefits

#### File Size Reduction
- **Original JSON**: ~3.1MB
- **MessagePack**: ~2.2MB (30% smaller)
- **Package size**: Significantly reduced

#### Loading Performance
- **JSON loading**: ~50-100ms
- **MessagePack loading**: ~30-60ms (40% faster)
- **Memory usage**: 20-30% less due to efficient encoding

#### Startup Impact
- **Total startup time**: Reduced from ~5s to ~3s
- **Memory footprint**: ~35MB instead of ~50MB
- **Parse overhead**: Minimal binary decoding vs text parsing

### Fallback Strategy

For maximum compatibility, include both formats:

```
data/
├── sessions.msgpack      # Primary format (fast loading)
└── sessions.json         # Fallback format (universal compatibility)
```

```python
# Python fallback loading
try:
    import msgpack
    with open('data/sessions.msgpack', 'rb') as f:
        data = msgpack.unpack(f, raw=False)
except (ImportError, FileNotFoundError):
    import json
    with open('data/sessions.json', 'r') as f:
        data = json.load(f)
```

This approach provides **optimal performance** while maintaining **universal compatibility**.
```javascript
// Simple in-memory structure
{
  sessions: Array<Session>  // Direct array of session objects
}

// Example search implementation
function searchSessions(query) {
  return sessions.filter(session => 
    session.title.toLowerCase().includes(query.toLowerCase()) ||
    session.abstract.toLowerCase().includes(query.toLowerCase()) ||
    session.speakers?.some(speaker => 
      speaker.toLowerCase().includes(query.toLowerCase())
    )
  );
}
```

### 3. Search Implementation
- **Full-text search**: Simple string matching on titles/abstracts
- **Category filtering**: Array filtering on embedded properties
- **Speaker search**: Array filtering on speakers array
- **Pagination**: Cursor-based using array slicing

## Testing Strategy

### Unit Testing Approach

#### 1. Data Layer Tests
- **Data loading**: Verify MessagePack loading
- **Data integrity**: Check session object structure

#### 2. Service Layer Tests
- **Search functionality**: Test string matching
- **Filter operations**: Verify array filtering
- **Pagination**: Test array slicing

#### 3. MCP Tool Tests
- **Tool registration**: Verify all tools are registered
- **Input validation**: Test schema validation
- **Output format**: Verify response structure

### Test Data Strategy
- **Subset testing**: Use smaller dataset for unit tests
- **Mock data**: Generate synthetic data for edge cases
- **Real data validation**: Test against actual session data

### Coverage Requirements
- **Minimum 90% code coverage**
- **All public APIs tested**
- **Error paths covered**
- **Performance benchmarks**

## Performance Considerations

### Memory Optimization
- **Direct array storage**: Minimal memory overhead
- **No duplicate data**: Single source of truth in session objects
- **MessagePack efficiency**: 30% smaller than JSON

### Search Performance
- **Linear search**: O(n) but fast for 1,843 sessions (<10ms)
- **Simple string matching**: No complex indexing overhead
- **Pagination**: Array slicing for result sets

### Startup Optimization
- **Fast loading**: Direct MessagePack deserialization
- **No preprocessing**: Load and use immediately
- **Minimal startup time**: <1 second for full dataset

## Error Handling

### Data Loading Errors
- **Invalid JSON**: Graceful fallback with error reporting
- **Missing fields**: Skip invalid records with warnings
- **Schema validation**: Validate data structure at load time

### Runtime Errors
- **Invalid session codes**: Return appropriate error messages
- **Search timeouts**: Implement query timeouts
- **Memory limits**: Monitor and report memory usage

### MCP Protocol Errors
- **Invalid requests**: Proper error responses
- **Tool not found**: Standard MCP error handling
- **Parameter validation**: Schema-based validation

## Deployment Considerations

### Package Distribution
- **Data bundling**: Include sessions.msgpack in package
- **Smaller size**: MessagePack reduces package size by 30%
- **Simple deployment**: No data transformation needed

### Runtime Requirements
- **Memory**: ~30MB for full dataset (reduced from 50MB)
- **Startup time**: <1 second for data loading (reduced from 5s)
- **Response time**: <10ms for typical queries

### Monitoring
- **Health checks**: Verify data integrity
- **Performance metrics**: Track query performance
- **Error logging**: Comprehensive error tracking
