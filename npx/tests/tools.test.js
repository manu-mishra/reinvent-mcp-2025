import { createSessionTools } from '../src/tools/sessionTools.js';
import { mockSessions } from './testData.js';

describe('MCP Tools', () => {
  let tools;

  beforeEach(() => {
    tools = createSessionTools(mockSessions);
  });

  test('should create all 13 tools', () => {
    expect(Object.keys(tools)).toHaveLength(13);
    expect(tools.search_sessions).toBeDefined();
    expect(tools.get_session_details).toBeDefined();
    expect(tools.list_categories).toBeDefined();
    expect(tools.search_speakers).toBeDefined();
  });

  describe('search_sessions tool', () => {
    test('should have correct schema', () => {
      const tool = tools.search_sessions;
      expect(tool.name).toBe('search_sessions');
      expect(tool.inputSchema.required).toContain('query');
    });

    test('should execute search', async () => {
      const result = await tools.search_sessions.handler({ query: 'AI' });
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });
  });

  describe('get_session_details tool', () => {
    test('should return session details', async () => {
      const result = await tools.get_session_details.handler({ session_code: 'AIM236-S' });
      expect(result.code).toBe('AIM236-S');
      expect(result.speakers[0].name).toBe('John Doe');
    });
  });

  describe('list_categories tool', () => {
    test('should list category values', async () => {
      const result = await tools.list_categories.handler({ category: 'levels' });
      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('300 – Advanced');
    });
  });

  describe('get_sessions_by_level tool', () => {
    test('should filter by level', async () => {
      const result = await tools.get_sessions_by_level.handler({ level: '300' });
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });
  });

  describe('search_speakers tool', () => {
    test('should find speakers by name', async () => {
      const result = await tools.search_speakers.handler({ speaker_name: 'John' });
      expect(result.speakers).toHaveLength(1);
      expect(result.speakers[0].name).toBe('John Doe');
      expect(result.speakers[0].sessions[0].code).toBe('AIM236-S');
    });
  });
});
