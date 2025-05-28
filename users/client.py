import logging

import httpx

logger = logging.getLogger(__name__)


class WeatherClient:
    BASE_URL = "http://api.openweathermap.org"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(base_url=self.BASE_URL, timeout=10.0)

    def get_weather_by_zip(self, zip_code: str) -> dict:
        url = f"/data/2.5/weather?zip={zip_code}&appid={self.api_key}"
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                logger.warning(f"ZIP code not found: {zip_code}")
                return {"error": True, "zip_code": zip_code}
            raise
