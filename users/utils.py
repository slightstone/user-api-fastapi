from users.models import UserCreateRequest, WeatherLocation


def to_firebase_dict(location: WeatherLocation, user: UserCreateRequest) -> dict:
    return {
        "name": user.name,
        "zip_code": user.zip_code,
        "latitude": str(location.coord.lat),
        "longitude": str(location.coord.lon),
        "timezone_offset_seconds": location.timezone_offset_seconds,
        "timezone": location.timezone_human_readable,
        "timezone_error": getattr(location, "timezone_error", False),
    }


def to_firebase_update_dict(location: WeatherLocation, updates: dict) -> dict:
    """Used when updating a user, if zip code has changed."""
    return {
        **updates,
        "latitude": str(location.coord.lat),
        "longitude": str(location.coord.lon),
        "timezone_offset_seconds": location.timezone_offset_seconds,
        "timezone": location.timezone_human_readable,
        "timezone_error": location.timezone_error,
    }
