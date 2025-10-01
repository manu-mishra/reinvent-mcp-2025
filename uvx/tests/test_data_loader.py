import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from reinvent_2025_mcp.data.loader import load_sessions

class TestDataLoader:
    @pytest.mark.asyncio
    async def test_loads_sessions_from_messagepack(self):
        sessions = await load_sessions()
        assert isinstance(sessions, list)
        assert len(sessions) > 1000
        
        # Check session structure
        session = sessions[0]
        assert 'code' in session
        assert 'title' in session
        assert 'abstract' in session
        assert 'attributes' in session

    @pytest.mark.asyncio
    async def test_loads_sessions_with_proper_attributes_structure(self):
        sessions = await load_sessions()
        session_with_attributes = next(s for s in sessions if s.get('attributes', {}).get('topics'))
        
        assert 'topics' in session_with_attributes['attributes']
        assert 'services' in session_with_attributes['attributes']
        assert 'level' in session_with_attributes['attributes']
        assert isinstance(session_with_attributes['attributes']['topics'], list)
