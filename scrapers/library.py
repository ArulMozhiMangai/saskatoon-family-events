import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_library_events(date="tomorrow", age_filter=None):
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
        elif date == "today":
            date_label = datetime.today().strftime("%B %#d")
        elif date == "thisweek":
            date_label = "This Week"
        else:
            date_label = date

        event_list = []
        for e in events:
            name = e.find('h3')
            time_div = e.find('div', class_='mt-3 date-times')
            time_col = time_div.find('div', class_='col-3') if time_div else None
            location = time_div.find('strong') if time_div else None

            # Age filter support
            ages_tag = e.find('p', class_='tag-group')
            ages = ages_tag.text.strip() if ages_tag else ""
            if age_filter and age_filter.lower() not in ages.lower():
                continue

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