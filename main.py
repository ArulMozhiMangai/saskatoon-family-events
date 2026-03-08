import json
import logging
from scrapers.library import scrape_library_events

# --- Logging setup ---
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def save_events(events, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=2)
        print(f"✅ Saved {len(events)} events to {filename}")
        logging.info(f"Saved {len(events)} events to {filename}")
    except Exception as ex:
        logging.error(f"Failed to save events: {ex}")
        print(f"❌ Could not save events: {ex}")

# --- Run ---
events = scrape_library_events("tomorrow")
save_events(events, "events.json")

# --- Load back and print ---
try:
    with open("events.json", "r", encoding='utf-8') as f:
        loaded = json.load(f)

    print("\n📂 Loaded from JSON:")
    date_str = loaded[0]["date"] if loaded else "Today"
    print(f"📚 SASKATOON LIBRARY EVENTS — Tomorrow ({date_str})")
    print("—" * 50)
    for i, e in enumerate(loaded, 1):
        print(f"{i}. {e['name']}")
        print(f"   📍 {e['location']} | 🕒 {e['time']}")
except Exception as ex:
    logging.error(f"Failed to load events.json: {ex}")
    print(f"❌ Could not load JSON: {ex}")
