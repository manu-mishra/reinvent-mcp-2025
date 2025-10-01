import sys
from pathlib import Path

# Add both src and tests to path
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir.parent / "src"))
sys.path.insert(0, str(test_dir))

import pytest
from mcp.types import Tool
from reinvent_2025_mcp.tools.session_tools import create_session_tools
from test_data import mock_sessions

class TestMCPIntegration:
    def setup_method(self):
        self.tools = create_session_tools(mock_sessions)

    def test_all_tools_have_required_fields(self):
        """Test that all tools have required MCP fields"""
        for tool_name, tool_data in self.tools.items():
            assert 'name' in tool_data
            assert 'description' in tool_data
            assert 'inputSchema' in tool_data
            assert 'handler' in tool_data
            
            # Test Tool object creation doesn't fail
            tool_obj = Tool(
                name=tool_data['name'],
                description=tool_data['description'],
                inputSchema=tool_data['inputSchema']
            )
            assert tool_obj.name == tool_name

    def test_tool_schemas_are_valid(self):
        """Test that all tool schemas are valid JSON Schema"""
        for tool_name, tool_data in self.tools.items():
            schema = tool_data['inputSchema']
            assert schema['type'] == 'object'
            assert 'properties' in schema
            
            if 'required' in schema:
                assert isinstance(schema['required'], list)
                # All required fields should exist in properties
                for req_field in schema['required']:
                    assert req_field in schema['properties']

    def test_tool_handlers_are_callable(self):
        """Test that all tool handlers are callable"""
        for tool_name, tool_data in self.tools.items():
            handler = tool_data['handler']
            assert callable(handler)

    def test_tool_execution_with_minimal_params(self):
        """Test tool execution with minimal required parameters"""
        # Test search_sessions
        result = self.tools['search_sessions']['handler']({'query': 'test'})
        assert isinstance(result, dict)
        assert 'items' in result
        assert 'total' in result
        
        # Test get_session_details
        result = self.tools['get_session_details']['handler']({'session_code': 'AIM236-S'})
        assert result is not None
        
        # Test list_categories
        result = self.tools['list_categories']['handler']({'category': 'levels'})
        assert isinstance(result, list)

    def test_tool_execution_with_optional_params(self):
        """Test tool execution with optional parameters"""
        result = self.tools['search_sessions']['handler']({
            'query': 'test',
            'limit': 5,
            'cursor': '0'
        })
        assert isinstance(result, dict)
        assert len(result['items']) <= 5

    def test_tool_descriptions_are_informative(self):
        """Test that tool descriptions contain helpful information"""
        for tool_name, tool_data in self.tools.items():
            description = tool_data['description']
            assert len(description) > 20  # Should be descriptive
            
            # Enum-based tools should mention supported values
            if 'enum' in str(tool_data['inputSchema']):
                # These tools should have examples in description
                enum_tools = ['get_sessions_by_role', 'get_sessions_by_industry', 
                             'get_sessions_by_level', 'get_sessions_by_topic']
                if tool_name in enum_tools:
                    assert 'Supported' in description or 'supported' in description

    def test_error_handling_in_tools(self):
        """Test that tools handle errors gracefully"""
        # Test with invalid parameters
        try:
            result = self.tools['get_session_details']['handler']({'session_code': 'INVALID'})
            assert result is None  # Should return None, not crash
        except Exception as e:
            pytest.fail(f"Tool should handle invalid input gracefully: {e}")

    def test_pagination_parameters_consistency(self):
        """Test that pagination parameters are consistent across tools"""
        paginated_tools = [name for name in self.tools.keys() 
                          if name.startswith('get_sessions_by_') or name.startswith('search_')]
        
        for tool_name in paginated_tools:
            if tool_name == 'get_session_details':  # This one doesn't have pagination
                continue
                
            schema = self.tools[tool_name]['inputSchema']
            properties = schema['properties']
            
            # Should have limit parameter
            if 'limit' in properties:
                limit_prop = properties['limit']
                assert limit_prop['type'] == 'number'
                assert 'minimum' in limit_prop
                assert 'maximum' in limit_prop
            
            # Should have cursor parameter
            if 'cursor' in properties:
                cursor_prop = properties['cursor']
                assert cursor_prop['type'] == 'string'
