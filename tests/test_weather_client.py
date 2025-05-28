from tests.conftest import my_vcr
from users.geocode import fetch_location_from_zip
from users.models import ErrorWeatherLocationModel, WeatherLocation


@my_vcr.use_cassette("valid_zip.yaml")
def test_fetch_location_valid_zip():
    location = fetch_location_from_zip("10001")  # New York ZIP
    assert isinstance(location, WeatherLocation)
    assert location.coord.lat is not None
    assert location.coord.lon is not None
    assert isinstance(location.timezone_offset_seconds, int)
    assert isinstance(location.timezone_human_readable, str)
    assert location.timezone_human_readable != ""
    assert not location.timezone_error


@my_vcr.use_cassette("nonexistent_zip.yaml")
def test_fetch_location_nonexistent_zip():
    location = fetch_location_from_zip(
        "99999"
    )  # Technically valid format, but not real
    assert isinstance(location, ErrorWeatherLocationModel)
    assert location.error is True
    assert location.zip_code == "99999"
    assert location.coord.lat == 9999.0
    assert location.coord.lon == 9999.0
    assert location.timezone_human_readable == "Unknown"
    assert location.timezone_error


def test_fetch_location_bad_format():
    location = fetch_location_from_zip("abcd")  # Invalid format
    assert isinstance(location, ErrorWeatherLocationModel)
    assert location.error is True
    assert location.zip_code == "abcd"
    assert location.coord.lat == 9999.0
    assert location.coord.lon == 9999.0
    assert location.timezone_human_readable == "Unknown"
    assert location.timezone_error
