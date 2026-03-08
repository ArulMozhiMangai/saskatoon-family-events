from bs4 import BeautifulSoup

# Read the local HTML file you already saved
with open('events.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
events = soup.find_all('div', class_='row event-series')

print(f"Found {len(events)} events")
for e in events:
    name = e.find('h3')
    time = e.find('div', class_='mt-3 date-times')
    print(name.text.strip() if name else 'No name')
    print(time.text.strip() if time else 'No time')
    print('---')