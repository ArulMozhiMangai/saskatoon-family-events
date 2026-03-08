import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_city_rec_events(date=None):
    url = "https://apps5.saskatoon.ca/app/qRecTracDropin/DropinPrograms"

    if date is None:
        date = datetime.today().strftime("%m/%d/%Y")

    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})['value']

        logging.info("Successfully grabbed VIEWSTATE token")

    except Exception as ex:
        logging.error(f"Failed to load City Rec page: {ex}")
        print(f"❌ Could not load City Rec page: {ex}")
        return []

    try:
        form_data = {
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstate_gen,
            '__EVENTVALIDATION': event_validation,
            'ctl00$MainContent$lstKeywordSearch': 'All',
            'ctl00$MainContent$Facility': 'All',
            'ctl00$MainContent$ProgramTypes': 'All',
            'ctl00$MainContent$SearchBy': 'radiobtnDaily',
            'ctl00$MainContent$BtnSearchPrograms': 'Search',
        }

        response = session.post(url, data=form_data, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', {'id': 'tpwebsearch_output_table'})
        if not table:
            logging.warning("No results table found on City Rec page")
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
                    "date": date,
                    "time": f"{begin_time} - {end_time}",
                    "location": location,
                    "source": "City Rec"
                })

        logging.info(f"Scraped {len(event_list)} City Rec events")
        return event_list

    except Exception as ex:
        logging.error(f"Failed to parse City Rec events: {ex}")
        print(f"❌ Unexpected error: {ex}")
        return []