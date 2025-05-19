import requests
import json

ZONE_CODES = [
    "TXZ213",  # Houston (Inland Harris)
    "TXZ214",  # Pearland (Inland Brazoria)
    "TXZ226",  # Angleton, Clute, Lake Jackson (Coastal Brazoria)
    "TXZ227",  # West Columbia (Inland Brazoria)
    "TXZ209",  # New Braunfels (Guadalupe County)
    "TXZ250",  # Crystal City (Zavala County)
    "TXZ230",  # Rocksprings (Edwards Plateau)
    "TXZ198",  # Huntsville (Walker County)
]

def get_first_alert():
    for zone in ZONE_CODES:
        try:
            res = requests.get(f"https://api.weather.gov/alerts/active/zone/{zone}", timeout=10)
            res.raise_for_status()
            alerts = res.json().get("features", [])
            if alerts:
                alert = alerts[0]["properties"]
                headline = alert["headline"]
                desc = alert["description"]
                area = alert["areaDesc"]
                message = f"⚠️ {headline}\n\n{desc}\n\n📍 {area}"
                return message
        except Exception as e:
            print(f"Error fetching zone {zone}: {e}")
    return ""

if __name__ == "__main__":
    alert_message = get_first_alert()
    if alert_message:
        # Output to GitHub Actions
        with open(os.environ["GITHUB_ENV"], "a") as env_file:
            env_file.write(f'ALERT_MESSAGE<<EOF\n{alert_message}\nEOF\n')
    else:
        print("No active alerts.")

