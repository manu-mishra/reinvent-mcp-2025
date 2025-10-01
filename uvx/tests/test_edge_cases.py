import sys
from pathlib import Path

# Add both src and tests to path
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir.parent / "src"))
sys.path.insert(0, str(test_dir))

import pytest
from reinvent_2025_mcp.services.session_service import SessionService
from test_data import mock_sessions

class TestEdgeCases:
    def setup_method(self):
        self.service = SessionService(mock_sessions)

    def test_empty_query_search(self):
        result = self.service.search_sessions('')
        # Empty query should return all sessions (not filtered)
        assert len(result['items']) == len(mock_sessions)

    def test_invalid_session_code(self):
        result = self.service.get_session_details('INVALID-CODE')
        assert result is None

    def test_invalid_category(self):
        result = self.service.list_categories('invalid_category')
        assert result == []

    def test_large_limit_pagination(self):
        result = self.service.search_sessions('session', 1000, 0)
        assert len(result['items']) <= len(mock_sessions)
        assert result['total'] == 2

    def test_cursor_beyond_results(self):
        result = self.service.search_sessions('session', 10, 100)
        assert len(result['items']) == 0
        assert result['hasMore'] is False
        assert result['nextCursor'] is None

    def test_search_with_special_characters(self):
        result = self.service.search_sessions('AI & ML')
        # Should not crash and return valid structure
        assert 'items' in result
        assert 'total' in result

    def test_empty_speakers_search(self):
        result = self.service.search_speakers('')
        # Empty speaker search should return speakers
        assert result['total'] >= 0
        assert 'speakers' in result

    def test_nonexistent_service_filter(self):
        result = self.service.get_sessions_by_service('NonExistent Service')
        assert len(result['items']) == 0
        assert result['total'] == 0

    def test_nonexistent_level_filter(self):
        result = self.service.get_sessions_by_level('999')
        assert len(result['items']) == 0

    def test_case_insensitive_search(self):
        result_upper = self.service.search_sessions('AI')
        result_lower = self.service.search_sessions('ai')
        assert result_upper['total'] == result_lower['total']

    def test_pagination_consistency(self):
        # Test that pagination returns consistent results
        page1 = self.service.search_sessions('session', 1, 0)
        page2 = self.service.search_sessions('session', 1, 1)
        
        if page1['items'] and page2['items']:
            assert page1['items'][0]['code'] != page2['items'][0]['code']

    def test_minimal_session_structure(self):
        result = self.service.search_sessions('AI')
        if result['items']:
            session = result['items'][0]
            assert 'code' in session
            assert 'title' in session
            assert 'abstract' in session

    def test_cleaned_session_details_structure(self):
        result = self.service.get_session_details('AIM236-S')
        assert result is not None
        
        # Check that unwanted fields are removed
        assert 'length' not in result
        assert 'sessionID' not in result
        assert 'eventId' not in result
        assert 'published' not in result
        assert 'modified' not in result
        
        # Check speaker cleaning
        if result['speakers']:
            speaker = result['speakers'][0]
            assert 'name' in speaker
            assert 'jobTitle' in speaker
            assert 'company' in speaker
            assert 'role' in speaker
