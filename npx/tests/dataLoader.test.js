import { loadSessions } from '../src/data/loader.js';

describe('Data Loader', () => {
  test('should load sessions from MessagePack', async () => {
    const sessions = await loadSessions();
    expect(Array.isArray(sessions)).toBe(true);
    expect(sessions.length).toBeGreaterThan(1000);
    
    // Check session structure
    const session = sessions[0];
    expect(session).toHaveProperty('code');
    expect(session).toHaveProperty('title');
    expect(session).toHaveProperty('abstract');
    expect(session).toHaveProperty('attributes');
  });

  test('should load sessions with proper attributes structure', async () => {
    const sessions = await loadSessions();
    const sessionWithAttributes = sessions.find(s => s.attributes?.topics?.length > 0);
    
    expect(sessionWithAttributes.attributes).toHaveProperty('topics');
    expect(sessionWithAttributes.attributes).toHaveProperty('services');
    expect(sessionWithAttributes.attributes).toHaveProperty('level');
    expect(Array.isArray(sessionWithAttributes.attributes.topics)).toBe(true);
  });
});
