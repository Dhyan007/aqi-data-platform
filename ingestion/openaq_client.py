
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")

BASE_URL = "https://api.openaq.org/v3"


def get_locations():
    if not API_KEY:
        raise ValueError(
            "OPENAQ_API_KEY is missing. Check your .env file."
        )

    url = f"{BASE_URL}/locations"

    headers = {
        "X-API-Key": API_KEY
    }

    params = {
        "iso": "IN",
        "limit": 100,
        "page": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()




def get_sensors(location_id):
    url = f"{BASE_URL}/locations/{location_id}/sensors"

    headers = {
        "X-API-Key": API_KEY
    }

    params = {
        "limit": 100,
        "page": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def get_hourly_measurements(
    sensor_id,
    datetime_from,
    datetime_to,
):
    url = f"{BASE_URL}/sensors/{sensor_id}/hours"

    headers = {
        "X-API-Key": API_KEY
    }

    params = {
        "datetime_from": datetime_from,
        "datetime_to": datetime_to,
        "limit": 100,
        "page": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()



if __name__ == "__main__":
    sensor_id = 30

    data = get_hourly_measurements(
        sensor_id=sensor_id,
        datetime_from="2026-10-01T00:00:00Z",
        datetime_to="2026-10-04T00:00:00Z",
    )

    meta = data.get("meta", {})
    measurements = data.get("results", [])

    print("Hourly data request successful!")
    print("Sensor ID:", sensor_id)
    print("Records found:", meta.get("found"))

    print("\nFirst 5 measurements:\n")

    for item in measurements[:5]:
        period = item.get("period", {})

        print(
            "Value:", item.get("value"),
            "| From:", period.get("datetimeFrom", {}).get("utc"),
            "| To:", period.get("datetimeTo", {}).get("utc"),
        )

