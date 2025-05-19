import json
import requests
import os

TOKEN = os.environ['NOTIFY_EVENTS_TOKEN']
HEADERS = {'User-Agent': 'ClaytonWeatherBot (contact@claytonweather.com)'}

def load_zones():
    with open('zones.txt') as f:
        return [line.strip() for line in f if line.strip()]

def load_sent_ids():
    if not os.path.exists('sent_ids.json'):
        return set()
    with open('sent_ids.json') as f:
        return set(json.load(f))

def save_sent_ids(ids):
    with open('sent_ids.json', 'w') as f:
        json.dump(list(ids), f)

def fetch_alerts(zone):
    url = f"https://api.weather.gov/alerts/active?zone={zone}"
    resp = requests.get(url, headers=HEADERS)
    return resp.json().get("features", [])

def send_alert(title, desc):
    payload = {
        "token": TOKEN,
        "title": title,
        "message": desc,
        "priority": 3
    }
    requests.post("https://notify.events/api/message", data=payload)

def main():
    zones = load_zones()
    sent_ids = load_sent_ids()
    new_sent_ids = set(sent_ids)

    for zone in zones:
        alerts = fetch_alerts(zone)
        for alert in alerts:
            alert_id = alert["id"]
            if alert_id not in sent_ids:
                props = alert["properties"]
                title = props.get("headline", "⚠️ New Weather Alert")
                desc = props.get("description", "See details at https://weather.gov")
                send_alert(title, desc)
                new_sent_ids.add(alert_id)

    save_sent_ids(new_sent_ids)

if __name__ == "__main__":
    main()
