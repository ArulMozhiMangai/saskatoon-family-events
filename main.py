import json
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# --- Logging setup ---
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_library_events(date="tomorrow"):
    try:
        with open('events.html', 'r', encoding='utf-8') as f:
            html = f.read()
        logging.info("Successfully read events.html")
    except FileNotFoundError:
        logging.error("events.html not found — did you save the page?")
        print("❌ Error: events.html not found. Please save the library page first.")
        return []

    try:
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.find_all('div', class_='row event-series')

        if not events:
            logging.warning("No events found — HTML structure may have changed")
            print("⚠️ No events found. The website structure may have changed.")
            return []

        if date == "tomorrow":
            date_label = (datetime.today() + timedelta(days=1)).strftime("%B %#d")
        else:
            date_label = date

        event_list = []
        for e in events:
            name = e.find('h3')
            time_div = e.find('div', class_='mt-3 date-times')
            time_col = time_div.find('div', class_='col-3') if time_div else None
            location = time_div.find('strong') if time_div else None

            event_list.append({
                "name": name.text.strip() if name else "Unknown",
                "date": date_label,
                "time": time_col.text.strip() if time_col else "Unknown",
                "location": location.text.strip() if location else "Unknown",
                "source": "Library"
            })

        logging.info(f"Scraped {len(event_list)} events successfully")
        return event_list

    except Exception as ex:
        logging.error(f"Unexpected error while parsing: {ex}")
        print(f"❌ Unexpected error: {ex}")
        return []

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
