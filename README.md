# Saskatoon Family Events

A Python web scraper that aggregates family-friendly events across Saskatoon 
from multiple sources into one unified daily view.

## How to install
```bash
pip install requests beautifulsoup4 playwright
python -m playwright install chromium
```

## How to run
```bash
# Tomorrow's events
python main.py --date tomorrow

# Today's events  
python main.py --date today

# Kids/family events only
python main.py --date tomorrow --kids-only
```

## Sample output
```
📅 SASKATOON EVENTS — Tomorrow (March 11)
——————————————————————————————————————————
  📚 Mindfully Unwinding Whiteness — Round Prairie Library | 1:30pm
  🏊 Shallow — Lawson Aqua Walk | 6:15 AM
  🏊 Lane Swim — Lakewood | 6:30 AM
```

## Project structure
- `main.py` — entry point, CLI arguments, unified output
- `scrapers/library.py` — Saskatoon Public Library scraper
- `scrapers/city_rec.py` — City of Saskatoon Rec scraper (Playwright)
- `requirements.txt` — project dependencies

## Sessions completed
- Sessions 1–5: Setup, fetching, BeautifulSoup parsing, structured dictionaries, clean output
- Sessions 6–7: JSON file I/O, error handling and logging
- Sessions 8–10: Refactored into modules, date and age filter parameters
- Sessions 11–14: City Rec scraper, Playwright, unified two-source event list
- Sessions 15–18: CLI arguments, kids filter, polish

## Built with
- Python 3
- requests
- BeautifulSoup4
- Playwright
