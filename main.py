import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_library_events(date="tomorrow"):
    with open('events.html', 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    events = soup.find_all('div', class_='row event-series')

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

    return event_list

def save_events(events, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2)
    print(f"✅ Saved {len(events)} events to {filename}")

# --- Run ---
events = scrape_library_events("tomorrow")
save_events(events, "events.json")

# --- Load back and confirm ---
with open("events.json", "r", encoding='utf-8') as f:
    loaded = json.load(f)

print("\n📂 Loaded from JSON:")
date_str = loaded[0]["date"] if loaded else "Today"
print(f"📚 SASKATOON LIBRARY EVENTS — Tomorrow ({date_str})")
print("—" * 50)
for i, e in enumerate(loaded, 1):
    print(f"{i}. {e['name']}")
    print(f"   📍 {e['location']} | 🕒 {e['time']}")
