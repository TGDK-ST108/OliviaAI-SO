import requests

class SatelliteDataFetcher:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_live_data(self, satellite_name, parameters):
        """Fetch live satellite data from OliviaAI's API."""
        url = f"{self.base_url}/retrieve-live-data"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"satellite": satellite_name, "parameters": parameters}
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.status_code, "message": response.text}

# Example usage
base_url = "https://api.olivia-tgdk.com"
api_key = "your_api_key_here"
satellite_name = "Landsat-8"

parameters = {
    "longitude": -95.33,
    "latitude": 29.78,
    "date": "2024-01-01",
    "resolution": "high"
}

fetcher = SatelliteDataFetcher(base_url, api_key)
data = fetcher.fetch_live_data(satellite_name, parameters)
print(data)