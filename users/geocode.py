from users.client import WeatherClient
from users.models import ErrorWeatherLocationModel, WeatherLocation
from users.settings import settings


def fetch_location_from_zip(
    zip_code: str,
) -> ErrorWeatherLocationModel | WeatherLocation:
    client = WeatherClient(api_key=settings.openweathermap_api_key)
    data = client.get_weather_by_zip(zip_code)

    if data.get("error") is True:
        return ErrorWeatherLocationModel(**data)

    return WeatherLocation(**data)
