# Test Suite

## Overview
Unit tests for the AWS re:Invent 2025 MCP Server covering all core functionality.

## Test Coverage
- **22 tests** across 3 test suites
- **SessionService**: Core business logic (12 tests)
- **MCP Tools**: Tool integration and schemas (8 tests) 
- **Data Loader**: MessagePack data loading (2 tests)

## Running Tests
```bash
pip install -e ".[test]"
pytest
```

## Test Structure

### SessionService Tests
- Search functionality (title, abstract, speaker)
- Session details retrieval
- Category filtering (level, role, topic)
- Category listing with counts
- Pagination logic

### MCP Tools Tests
- Tool creation and schema validation
- Tool execution and response format
- All 13 tools registered correctly
- Parameter validation

### Data Loader Tests
- MessagePack file loading
- Session data structure validation
- Real data integration (1843 sessions)

## Test Data
Uses minimal mock data (`test_data.py`) for unit tests and real MessagePack data for integration tests.

## Results
✅ All 22 tests passing
✅ 100% core functionality covered
✅ Real data integration verified
