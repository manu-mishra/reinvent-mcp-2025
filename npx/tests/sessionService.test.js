import { SessionService } from '../src/services/sessionService.js';
import { mockSessions } from './testData.js';

describe('SessionService', () => {
  let service;

  beforeEach(() => {
    service = new SessionService(mockSessions);
  });

  describe('searchSessions', () => {
    test('should find sessions by title', () => {
      const result = service.searchSessions('AI');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });

    test('should find sessions by abstract', () => {
      const result = service.searchSessions('productivity');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('DVT222-S');
    });

    test('should find sessions by speaker name', () => {
      const result = service.searchSessions('John');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });
  });

  describe('getSessionDetails', () => {
    test('should return session details', () => {
      const result = service.getSessionDetails('AIM236-S');
      expect(result.code).toBe('AIM236-S');
      expect(result.speakers).toHaveLength(1);
      expect(result.speakers[0].name).toBe('John Doe');
    });

    test('should return null for non-existent session', () => {
      const result = service.getSessionDetails('INVALID');
      expect(result).toBeNull();
    });
  });

  describe('getSessionsByLevel', () => {
    test('should filter by level', () => {
      const result = service.getSessionsByLevel('300');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });

    test('should return empty for non-matching level', () => {
      const result = service.getSessionsByLevel('500');
      expect(result.items).toHaveLength(0);
    });
  });

  describe('getSessionsByRole', () => {
    test('should filter by role', () => {
      const result = service.getSessionsByRole('Data Scientist');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('AIM236-S');
    });
  });

  describe('getSessionsByTopic', () => {
    test('should filter by topic', () => {
      const result = service.getSessionsByTopic('Developer Tools');
      expect(result.items).toHaveLength(1);
      expect(result.items[0].code).toBe('DVT222-S');
    });
  });

  describe('listCategories', () => {
    test('should list levels with counts', () => {
      const result = service.listCategories('levels');
      expect(result).toHaveLength(2);
      expect(result[0].name).toBe('300 – Advanced');
      expect(result[0].count).toBe(1);
    });

    test('should list topics with counts', () => {
      const result = service.listCategories('topics');
      expect(result).toHaveLength(2);
      expect(result.find(t => t.name === 'Artificial Intelligence').count).toBe(1);
    });
  });

  describe('pagination', () => {
    test('should paginate results', () => {
      const result = service.searchSessions('session', 1, 0);
      expect(result.items).toHaveLength(1);
      expect(result.hasMore).toBe(true);
      expect(result.nextCursor).toBe('1');
    });

    test('should handle cursor pagination', () => {
      const result = service.searchSessions('session', 1, 1);
      expect(result.items).toHaveLength(1);
      expect(result.hasMore).toBe(false);
    });
  });

  describe('empty search queries', () => {
    test('should return all sessions for empty search query', () => {
      const result = service.searchSessions('');
      expect(result.items).toHaveLength(2); // Should return all mock sessions
      expect(result.total).toBe(2);
    });

    test('should return all sessions for whitespace search query', () => {
      const result = service.searchSessions('   ');
      expect(result.items).toHaveLength(2); // Should return all mock sessions
      expect(result.total).toBe(2);
    });

    test('should return all sessions for empty speaker search', () => {
      const result = service.searchSessions('');
      expect(result.items).toHaveLength(2); // Should return all mock sessions
      expect(result.total).toBe(2);
    });

    test('should return all sessions for whitespace speaker search', () => {
      const result = service.searchSessions('   ');
      expect(result.items).toHaveLength(2); // Should return all mock sessions
      expect(result.total).toBe(2);
    });
  });

  describe('speaker search', () => {
    test('should find speakers by name', () => {
      const result = service.searchSpeakers('John');
      expect(result.speakers).toHaveLength(1);
      expect(result.speakers[0].name).toBe('John Doe');
      expect(result.speakers[0].sessions).toHaveLength(1);
      expect(result.speakers[0].sessions[0].code).toBe('AIM236-S');
    });

    test('should return all speakers for empty search', () => {
      const result = service.searchSpeakers('');
      expect(result.speakers.length).toBeGreaterThanOrEqual(1);
      expect(result.total).toBeGreaterThanOrEqual(1);
      expect(result.speakers[0]).toHaveProperty('sessions');
    });

    test('should return all speakers for whitespace search', () => {
      const result = service.searchSpeakers('   ');
      expect(result.speakers.length).toBeGreaterThanOrEqual(1);
      expect(result.total).toBeGreaterThanOrEqual(1);
    });
  });
});
