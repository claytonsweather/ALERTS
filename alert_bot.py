import requests
import json
import os

# === CONFIGURATION ===
ZONE_CODES = ["TXZ213", "TXZ214", "TXZ215"]  # Add your desired zones
NOTIFY_EVENTS_URL = os.getenv("NOTIFY_EVENTS_URL")
SENT_ALERTS_FILE = "sent_alerts.json"

def load_sent_alerts():
    if os.path.exists(SENT_ALERTS_FILE):
        with open(SENT_ALERTS_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_sent_alerts(alert_ids):
    with open(SENT_ALERTS_FILE, "w") as f:
        json.dump(list(alert_ids), f)

def get_alerts():
    alerts = []
    for zone in ZONE_CODES:
        url = f"https://api.weather.gov/alerts/active/zone/{zone}"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            data = res.json()
            alerts.extend(data.get("features", []))
        except Exception as e:
            print(f"Error fetching zone {zone}: {e}")
    return alerts

def send_notification(message):
    if NOTIFY_EVENTS_URL:
        try:
            requests.post(NOTIFY_EVENTS_URL, data={"message": message})
        except Exception as e:
            print(f"Failed to send notification: {e}")

def main():
    sent_ids = load_sent_alerts()
    new_ids = set(sent_ids)

    alerts = get_alerts()
    for alert in alerts:
        alert_id = alert["id"]
        if alert_id not in sent_ids:
            props = alert["properties"]
            title = props["headline"]
            description = props["description"]
            area_desc = props["areaDesc"]
            message = f"⚠️ **{title}**\n\n{description}\n\n📍 {area_desc}"
            send_notification(message)
            new_ids.add(alert_id)

    save_sent_alerts(new_ids)

if __name__ == "__main__":
    main()
