
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

# --- Run & print nicely ---
events = scrape_library_events("tomorrow")
date_str = events[0]["date"] if events else "Today"

print(f"📚 SASKATOON LIBRARY EVENTS — Tomorrow ({date_str})")
print("—" * 50)
for i, e in enumerate(events, 1):
    print(f"{i}. {e['name']}")
    print(f"   📍 {e['location']} | 🕒 {e['time']}")
