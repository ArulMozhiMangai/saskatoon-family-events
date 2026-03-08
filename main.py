from bs4 import BeautifulSoup

with open('events.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
events = soup.find_all('div', class_='row event-series')

print(f"Found {len(events)} events\n")

event_list = []
for e in events:
    name = e.find('h3')
    time_div = e.find('div', class_='mt-3 date-times')
    time_col = time_div.find('div', class_='col-3') if time_div else None
    location = time_div.find('strong') if time_div else None  # ← moved here

    event = {
        "name": name.text.strip() if name else "Unknown",
        "location": location.text.strip() if location else "Unknown",
        "time": time_col.text.strip() if time_col else "Unknown",
    }
    event_list.append(event)
    print(event)
