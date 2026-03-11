import json
import logging
from scrapers.library import scrape_library_events

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

def print_events(events, label):
    date_str = events[0]["date"] if events else "Today"
    print(f"\n📚 SASKATOON LIBRARY EVENTS — {label} ({date_str})")
    print("—" * 50)
    if not events:
        print("No events found.")
        return
    for i, e in enumerate(events, 1):
        print(f"{i}. {e['name']}")
        print(f"   📍 {e['location']} | 🕒 {e['time']}")

# --- Test different parameters ---
print_events(scrape_library_events("tomorrow"), "Tomorrow")
print_events(scrape_library_events("today"), "Today")
print_events(scrape_library_events("tomorrow", age_filter="Kids"), "Kids Events")

save_events(scrape_library_events("tomorrow"), "events.json")

from scrapers.city_rec import scrape_city_rec_events

# Test City Rec
print("🔍 Fetching City Rec events...")
city_events = scrape_city_rec_events("tomorrow")
print(f"Got {len(city_events)} city events")
print(f"\n🏊 SASKATOON CITY REC EVENTS")
print("—" * 50)
if city_events:
    for i, e in enumerate(city_events, 1):
        print(f"{i}. {e['name']}")
        print(f"   📍 {e['location']} | 🕒 {e['time']}")
else:
    print("No events found.")