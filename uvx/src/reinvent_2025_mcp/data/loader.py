import msgpack
import sys
from pathlib import Path

async def load_sessions():
    """Load sessions from MessagePack file."""
    try:
        data_path = Path(__file__).parent / "sessions.msgpack"
        with open(data_path, 'rb') as f:
            data = msgpack.unpack(f, raw=False, strict_map_key=False)
        
        print(f"Loaded {len(data)} sessions from MessagePack", file=sys.stderr)
        return data
    except Exception as error:
        print(f"Failed to load sessions: {error}", file=sys.stderr)
        raise
