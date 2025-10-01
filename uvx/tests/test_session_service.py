import sys
from pathlib import Path

# Add both src and tests to path
test_dir = Path(__file__).parent
sys.path.insert(0, str(test_dir.parent / "src"))
sys.path.insert(0, str(test_dir))

import pytest
from reinvent_2025_mcp.services.session_service import SessionService
from test_data import mock_sessions

class TestSessionService:
    def setup_method(self):
        self.service = SessionService(mock_sessions)

    def test_search_sessions_by_title(self):
        result = self.service.search_sessions('AI')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'AIM236-S'

    def test_search_sessions_by_abstract(self):
        result = self.service.search_sessions('productivity')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'DVT222-S'

    def test_search_sessions_by_speaker_name(self):
        result = self.service.search_sessions('John')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'AIM236-S'

    def test_get_session_details_exists(self):
        result = self.service.get_session_details('AIM236-S')
        assert result['code'] == 'AIM236-S'
        assert len(result['speakers']) == 1
        assert result['speakers'][0]['name'] == 'John Doe'

    def test_get_session_details_not_exists(self):
        result = self.service.get_session_details('INVALID')
        assert result is None

    def test_get_sessions_by_level(self):
        result = self.service.get_sessions_by_level('300')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'AIM236-S'

    def test_get_sessions_by_level_no_match(self):
        result = self.service.get_sessions_by_level('500')
        assert len(result['items']) == 0

    def test_get_sessions_by_role(self):
        result = self.service.get_sessions_by_role('Data Scientist')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'AIM236-S'

    def test_get_sessions_by_topic(self):
        result = self.service.get_sessions_by_topic('Developer Tools')
        assert len(result['items']) == 1
        assert result['items'][0]['code'] == 'DVT222-S'

    def test_list_categories_levels(self):
        result = self.service.list_categories('levels')
        assert len(result) == 2
        level_names = [item['name'] for item in result]
        assert '300 – Advanced' in level_names
        assert '200 – Intermediate' in level_names
        # Check that each level has count of 1
        for item in result:
            assert item['count'] == 1

    def test_list_categories_topics(self):
        result = self.service.list_categories('topics')
        assert len(result) == 2
        ai_topic = next(t for t in result if t['name'] == 'Artificial Intelligence')
        assert ai_topic['count'] == 1

    def test_pagination_first_page(self):
        result = self.service.search_sessions('session', 1, 0)
        assert len(result['items']) == 1
        assert result['hasMore'] is True
        assert result['nextCursor'] == '1'

    def test_pagination_second_page(self):
        result = self.service.search_sessions('session', 1, 1)
        assert len(result['items']) == 1
        assert result['hasMore'] is False

    def test_search_sessions_empty_query_returns_all(self):
        result = self.service.search_sessions('')
        assert len(result['items']) == 2  # Should return all mock sessions
        assert result['total'] == 2

    def test_search_sessions_whitespace_query_returns_all(self):
        result = self.service.search_sessions('   ')
        assert len(result['items']) == 2  # Should return all mock sessions
        assert result['total'] == 2

    def test_search_sessions_by_speaker_empty_name_returns_all(self):
        result = self.service.search_sessions('')
        assert len(result['items']) == 2  # Should return all mock sessions
        assert result['total'] == 2

    def test_search_sessions_by_speaker_whitespace_name_returns_all(self):
        result = self.service.search_sessions('   ')
        assert len(result['items']) == 2  # Should return all mock sessions
        assert result['total'] == 2

    def test_search_speakers_with_name(self):
        result = self.service.search_speakers('John')
        assert len(result['speakers']) == 1
        assert result['speakers'][0]['name'] == 'John Doe'
        assert len(result['speakers'][0]['sessions']) == 1
        assert result['speakers'][0]['sessions'][0]['code'] == 'AIM236-S'

    def test_search_speakers_empty_name_returns_all(self):
        result = self.service.search_speakers('')
        assert len(result['speakers']) >= 1  # Should return speakers
        assert result['total'] >= 1
        assert 'sessions' in result['speakers'][0]

    def test_search_speakers_whitespace_name_returns_all(self):
        result = self.service.search_speakers('   ')
        assert len(result['speakers']) >= 1  # Should return speakers
        assert result['total'] >= 1
