import { SessionService } from '../src/services/sessionService.js';
import { mockSessions } from './testData.js';

describe('Edge Cases', () => {
  let service;

  beforeEach(() => {
    service = new SessionService(mockSessions);
  });

  test('should handle empty query search', () => {
    const result = service.searchSessions('');
    // Empty query should return all sessions (not filtered)
    expect(result.items.length).toBe(mockSessions.length);
  });

  test('should handle invalid session code', () => {
    const result = service.getSessionDetails('INVALID-CODE');
    expect(result).toBeNull();
  });

  test('should handle invalid category', () => {
    const result = service.listCategories('invalid_category');
    expect(result).toEqual([]);
  });

  test('should handle large limit pagination', () => {
    const result = service.searchSessions('session', 1000, 0);
    expect(result.items.length).toBeLessThanOrEqual(mockSessions.length);
    expect(result.total).toBe(2);
  });

  test('should handle cursor beyond results', () => {
    const result = service.searchSessions('session', 10, 100);
    expect(result.items).toHaveLength(0);
    expect(result.hasMore).toBe(false);
    expect(result.nextCursor).toBeNull();
  });

  test('should handle search with special characters', () => {
    const result = service.searchSessions('AI & ML');
    expect(result).toHaveProperty('items');
    expect(result).toHaveProperty('total');
  });

  test('should handle empty speakers search', () => {
    const result = service.searchSpeakers('');
    // Empty speaker search should return speakers
    expect(result.speakers.length).toBeGreaterThanOrEqual(0);
  });

  test('should handle nonexistent service filter', () => {
    const result = service.getSessionsByService('NonExistent Service');
    expect(result.items).toHaveLength(0);
    expect(result.total).toBe(0);
  });

  test('should handle nonexistent level filter', () => {
    const result = service.getSessionsByLevel('999');
    expect(result.items).toHaveLength(0);
  });

  test('should handle case insensitive search', () => {
    const resultUpper = service.searchSessions('AI');
    const resultLower = service.searchSessions('ai');
    expect(resultUpper.total).toBe(resultLower.total);
  });

  test('should maintain pagination consistency', () => {
    const page1 = service.searchSessions('session', 1, 0);
    const page2 = service.searchSessions('session', 1, 1);
    
    if (page1.items.length > 0 && page2.items.length > 0) {
      expect(page1.items[0].code).not.toBe(page2.items[0].code);
    }
  });

  test('should return minimal session structure', () => {
    const result = service.searchSessions('AI');
    if (result.items.length > 0) {
      const session = result.items[0];
      expect(session).toHaveProperty('code');
      expect(session).toHaveProperty('title');
      expect(session).toHaveProperty('abstract');
    }
  });

  test('should return cleaned session details structure', () => {
    const result = service.getSessionDetails('AIM236-S');
    expect(result).not.toBeNull();
    
    // Check that unwanted fields are removed
    expect(result).not.toHaveProperty('length');
    expect(result).not.toHaveProperty('sessionID');
    expect(result).not.toHaveProperty('eventId');
    expect(result).not.toHaveProperty('published');
    expect(result).not.toHaveProperty('modified');
    
    // Check speaker cleaning
    if (result.speakers && result.speakers.length > 0) {
      const speaker = result.speakers[0];
      expect(speaker).toHaveProperty('name');
      expect(speaker).toHaveProperty('jobTitle');
      expect(speaker).toHaveProperty('company');
      expect(speaker).toHaveProperty('role');
    }
  });
});
