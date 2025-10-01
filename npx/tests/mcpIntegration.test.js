import { createSessionTools } from '../src/tools/sessionTools.js';
import { mockSessions } from './testData.js';

describe('MCP Integration', () => {
  let tools;

  beforeEach(() => {
    tools = createSessionTools(mockSessions);
  });

  test('should have all tools with required fields', () => {
    for (const [toolName, toolData] of Object.entries(tools)) {
      expect(toolData).toHaveProperty('name');
      expect(toolData).toHaveProperty('description');
      expect(toolData).toHaveProperty('inputSchema');
      expect(toolData).toHaveProperty('handler');
      expect(toolData.name).toBe(toolName);
    }
  });

  test('should have valid tool schemas', () => {
    for (const [toolName, toolData] of Object.entries(tools)) {
      const schema = toolData.inputSchema;
      expect(schema.type).toBe('object');
      expect(schema).toHaveProperty('properties');
      
      if (schema.required) {
        expect(Array.isArray(schema.required)).toBe(true);
        // All required fields should exist in properties
        for (const reqField of schema.required) {
          expect(schema.properties).toHaveProperty(reqField);
        }
      }
    }
  });

  test('should have callable tool handlers', () => {
    for (const [toolName, toolData] of Object.entries(tools)) {
      expect(typeof toolData.handler).toBe('function');
    }
  });

  test('should execute tools with minimal parameters', async () => {
    // Test search_sessions
    const searchResult = await tools.search_sessions.handler({ query: 'test' });
    expect(searchResult).toHaveProperty('items');
    expect(searchResult).toHaveProperty('total');
    
    // Test get_session_details
    const detailsResult = await tools.get_session_details.handler({ session_code: 'AIM236-S' });
    expect(detailsResult).not.toBeNull();
    
    // Test list_categories
    const categoriesResult = await tools.list_categories.handler({ category: 'levels' });
    expect(Array.isArray(categoriesResult)).toBe(true);
  });

  test('should execute tools with optional parameters', async () => {
    const result = await tools.search_sessions.handler({
      query: 'test',
      limit: 5,
      cursor: '0'
    });
    expect(result).toHaveProperty('items');
    expect(result.items.length).toBeLessThanOrEqual(5);
  });

  test('should have informative tool descriptions', () => {
    for (const [toolName, toolData] of Object.entries(tools)) {
      const description = toolData.description;
      expect(description.length).toBeGreaterThan(20);
      
      // Enum-based tools should mention supported values
      const enumTools = ['get_sessions_by_role', 'get_sessions_by_industry', 
                        'get_sessions_by_level', 'get_sessions_by_topic'];
      if (enumTools.includes(toolName)) {
        expect(description.toLowerCase()).toMatch(/supported/);
      }
    }
  });

  test('should handle errors gracefully', async () => {
    // Test with invalid parameters
    const result = await tools.get_session_details.handler({ session_code: 'INVALID' });
    expect(result).toBeNull(); // Should return null, not crash
  });

  test('should have consistent pagination parameters', () => {
    const paginatedTools = Object.keys(tools).filter(name => 
      name.startsWith('get_sessions_by_') || name.startsWith('search_')
    );
    
    for (const toolName of paginatedTools) {
      if (toolName === 'get_session_details') continue; // No pagination
      
      const schema = tools[toolName].inputSchema;
      const properties = schema.properties;
      
      // Should have limit parameter
      if (properties.limit) {
        expect(properties.limit.type).toBe('number');
        expect(properties.limit).toHaveProperty('minimum');
        expect(properties.limit).toHaveProperty('maximum');
      }
      
      // Should have cursor parameter
      if (properties.cursor) {
        expect(properties.cursor.type).toBe('string');
      }
    }
  });
});
