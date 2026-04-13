import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from dotenv import load_dotenv
import os

# Load .env explicitly
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_events_email(events, date_label):
    if not events:
        print("No events to send.")
        return

    # Build email body
    body = f"📅 SASKATOON EVENTS — {date_label}\n"
    body += "—" * 40 + "\n\n"
    for e in events:
        icon = "📚" if e["source"] == "Library" else "🏊"
        time = e["time"].split(" - ")[0]
        body += f"{icon} {e['name']}\n"
        body += f"   📍 {e['location']} | 🕒 {time}\n\n"

    # Build email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"Saskatoon Family Events — {date_label}"
    msg.attach(MIMEText(body, 'plain'))

    # Send
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent to {EMAIL_TO}")
    except Exception as ex:
        print(f"❌ Failed to send email: {ex}")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from scrapers.library import scrape_library_events
    from scrapers.city_rec import scrape_city_rec_events
    from datetime import datetime

    date = "today"
    date_label = datetime.today().strftime("%B %#d")

    print("🔍 Fetching library events...")
    library_events = scrape_library_events(date)

    print("🔍 Fetching City Rec events...")
    city_events = scrape_city_rec_events(date)

    all_events = library_events + city_events
    print(f"📬 Sending {len(all_events)} events...")
    send_events_email(all_events, f"Today ({date_label})")