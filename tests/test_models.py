from decimal import Decimal

import pytest
from pydantic import ValidationError

from users.models import (
    Coord,
    ErrorWeatherLocationModel,
    UserCreateRequest,
    WeatherLocation,
)


def test_valid_zip_code():
    req = UserCreateRequest(name="Test User", zip_code="12345-6789")
    assert req.zip_code == "12345-6789"


def test_invalid_zip_code():
    with pytest.raises(ValidationError):
        UserCreateRequest(name="Test User", zip_code="ABCDE")


def test_timezone_resolves_successfully():
    loc = WeatherLocation(
        coord=Coord(lat=Decimal("40.7128"), lon=Decimal("-74.0060")),  # New York
        timezone=0,
    )
    assert loc.timezone_human_readable != "Unknown"
    assert loc.timezone_error is False


def test_timezone_fails_and_sets_flags():
    loc = WeatherLocation(
        coord=Coord(lat=Decimal("9999.0"), lon=Decimal("9999.0")), timezone=0
    )
    assert loc.timezone_human_readable == "Unknown"
    assert loc.timezone_error is True


def test_error_weather_location_defaults():
    err = ErrorWeatherLocationModel(zip_code="00000")
    assert err.error is True
    assert err.coord.lat == Decimal("9999.0")
    assert err.coord.lon == Decimal("9999.0")
    assert err.timezone_offset_seconds == 0
    assert err.timezone_human_readable == "Unknown"
