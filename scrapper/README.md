# AWS re:Invent 2025 Session Scraper

Python scraper using Playwright to extract all 1800+ sessions from the AWS re:Invent 2025 event catalog.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Usage

**Scrape sessions:**
```bash
python reinvent_scraper.py
```

**Process data by attributes:**
```bash
python data_processor.py
```

## Output

- `../data/sessions.json` - All 1843 sessions with structured data
- `../data/*/` - Organized folders by attribute (roles, segments, topics, services, etc.)

## Session Data Fields

Each session includes 40+ attributes:
- `code` - Session ID (e.g., DVT222-S)
- `title` - Session title  
- `abstract` - Description
- `type` - Session type
- `sessionID` - Unique identifier
- Plus scheduling, metadata, and access control fields
