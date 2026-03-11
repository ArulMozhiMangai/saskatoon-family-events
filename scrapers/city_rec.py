import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def scrape_city_rec_events(date="tomorrow"):
    if date == "tomorrow":
        target = datetime.today() + timedelta(days=1)
    elif date == "today":
        target = datetime.today()
    else:
        target = datetime.strptime(date, "%Y-%m-%d")

    day = str(target.day)
    date_label = target.strftime("%B %#d")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # visible so we can see what happens
            page = browser.new_page()
            page.goto("https://apps5.saskatoon.ca/app/qRecTracDropin/DropinPrograms")
            page.wait_for_load_state("networkidle")

            # Click the correct day in the calendar table
            page.locator(f"table td a:has-text('{day}')").first.click()
            
            # Wait for results text then scroll to load table
            page.wait_for_load_state("load")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='table')

        if not table:
            print("⚠️ No results table found.")
            return []

        rows = table.find('tbody').find_all('tr')
        event_list = []

        for row in rows:
            cells = row.find_all('td', class_='label-cell')
            if len(cells) >= 3:
                description = cells[0].text.strip()
                begin_time = cells[1].text.strip()
                end_time = cells[2].text.strip()

                if ' - ' in description:
                    parts = description.split(' - ', 1)
                    location = parts[0].strip()
                    name = parts[1].strip()
                else:
                    location = "City Rec"
                    name = description

                event_list.append({
                    "name": name,
                    "date": date_label,
                    "time": f"{begin_time} - {end_time}",
                    "location": location,
                    "source": "City Rec"
                })

        logging.info(f"Scraped {len(event_list)} City Rec events")
        return event_list

    except Exception as ex:
        logging.error(f"Failed to scrape City Rec: {ex}")
        print(f"❌ Error scraping City Rec: {ex}")
        return []