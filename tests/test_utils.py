from decimal import Decimal

from users.models import UserCreateRequest, WeatherLocation
from users.utils import to_firebase_dict, to_firebase_update_dict


def test_to_firebase_dict_conversion():
    user = UserCreateRequest(name="Sam", zip_code="90210")
    location = WeatherLocation(
        coord={"lat": Decimal("34.0901"), "lon": Decimal("-118.4065")},
        timezone_offset_seconds=-28800,
        timezone_human_readable="America/Los_Angeles",
        timezone_error=False,
    )

    firebase_data = to_firebase_dict(location, user)

    assert firebase_data["name"] == "Sam"
    assert firebase_data["zip_code"] == "90210"
    assert firebase_data["latitude"] == "34.0901"
    assert firebase_data["longitude"] == "-118.4065"
    assert firebase_data["timezone_offset_seconds"] == -28800
    assert firebase_data["timezone"] == "America/Los_Angeles"
    assert firebase_data["timezone_error"] is False


def test_to_firebase_update_dict_conversion():
    updates = {"zip_code": "10001", "name": "Updated Name"}
    location = WeatherLocation(
        coord={"lat": Decimal("40.75"), "lon": Decimal("-73.99")},
        timezone_offset_seconds=-18000,
        timezone_human_readable="America/New_York",
        timezone_error=False,
    )

    result = to_firebase_update_dict(location, updates)

    assert result["zip_code"] == "10001"
    assert result["name"] == "Updated Name"
    assert result["latitude"] == "40.75"
    assert result["longitude"] == "-73.99"
    assert result["timezone_offset_seconds"] == -18000
    assert result["timezone"] == "America/New_York"
    assert result["timezone_error"] is False
