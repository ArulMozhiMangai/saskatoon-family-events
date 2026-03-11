import json
import logging
from scrapers.library import scrape_library_events
from scrapers.city_rec import scrape_city_rec_events

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

def sort_key(event):
    # Convert time string to sortable format
    try:
        time_str = event["time"].split(" - ")[0].strip()
        return time_str
    except:
        return "99:99"

def print_unified(events, date_label):
    print(f"\n📅 SASKATOON EVENTS — {date_label}")
    print("—" * 50)
    if not events:
        print("No events found.")
        return
    for e in events:
        icon = "📚" if e["source"] == "Library" else "🏊"
        time = e["time"].split(" - ")[0]  # just start time
        print(f"  {icon} {e['name']} — {e['location']} | {time}")

# --- Fetch from both sources ---
print("🔍 Fetching library events...")
library_events = scrape_library_events("tomorrow")

print("🔍 Fetching City Rec events...")
city_events = scrape_city_rec_events("tomorrow")

# --- Combine and sort ---
all_events = library_events + city_events
all_events.sort(key=sort_key)

# --- Print unified view ---
from datetime import datetime, timedelta
date_label = (datetime.today() + timedelta(days=1)).strftime("%B %#d")
print_unified(all_events, f"Tomorrow ({date_label})")

# --- Save to JSON ---
save_events(all_events, "events.json")
