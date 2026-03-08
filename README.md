# Saskatoon Family Events 

A Python web scraper that aggregates family-friendly events across Saskatoon 
from multiple sources into one unified daily view.

## What it does
Scrapes the Saskatoon Public Library events page and displays today's or 
tomorrow's events in a clean, readable format.

## How to run
```bash
python main.py
```

## Sample output
```
📚 SASKATOON LIBRARY EVENTS — Tomorrow (March 9)
——————————————————————————————————————————————
1. Mindfully Unwinding Whiteness
   📍 Round Prairie Library | 🕒 1:30pm to 3:45pm
```

## Project structure
- `main.py` — main scraper and output formatter
- `events.html` — locally saved library events page (update daily until 
  live fetching is implemented)

## Sessions completed
- Sessions 1–5: Setup, fetching, BeautifulSoup parsing, structured 
  dictionaries, clean formatted output
- Sessions 6–7: JSON file I/O, error handling and logging
- Sessions 8–10: Refactored into modules, date and age filter parameters

## Built with
- Python 3
- requests
- BeautifulSoup4

## Project structure
- `main.py` — entry point, prints and saves events
- `scrapers/library.py` — Saskatoon Library scraper
- `scrapers/__init__.py` — makes scrapers a Python package
- `requirements.txt` — project dependencies
- `events.html` — locally saved library page (temporary, gitignored)
- `events.json` — generated output (gitignored)
- `scraper.log` — error log (gitignored)