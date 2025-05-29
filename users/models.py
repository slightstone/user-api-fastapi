import logging
import re
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from timezonefinder import TimezoneFinder

logger = logging.getLogger(__name__)


class UserCreateRequest(BaseModel):
    name: str = Field(..., description="Full name of the user")
    zip_code: str = Field(
        ...,
        min_length=5,
        max_length=10,
        description="US ZIP code (5 or 9 digit format)",
    )

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()

    @field_validator("zip_code")
    @classmethod
    def validate_zip_code(cls, v: str) -> str:
        """Ensure the ZIP code is a valid 5-digit or 9-digit US ZIP code."""
        if not re.fullmatch(r"^\d{5}(-\d{4})?$", v):
            raise ValueError("Invalid US ZIP code format")
        return v


class UserUpdateRequest(UserCreateRequest):
    name: str | None = None
    zip_code: str | None = Field(
        default=None,
        min_length=5,
        max_length=10,
        description="US ZIP code (5 or 9 digit format)",
    )


class Coord(BaseModel):
    lon: Decimal = Field(..., description="Longitude as a decimal number")
    lat: Decimal = Field(..., description="Latitude as a decimal number")


class WeatherLocation(BaseModel):
    coord: Coord = Field(..., description="Geographical coordinates")
    timezone_offset_seconds: int = Field(
        ..., alias="timezone", description="Timezone offset in seconds from UTC"
    )
    timezone_human_readable: str = Field(
        default="",
        description="Human-readable timezone string (e.g., 'America/New_York')",
    )
    timezone_error: bool = Field(
        default=False, description="True if timezone resolution failed"
    )

    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="after")
    def resolve_timezone(self) -> "WeatherLocation":
        """Attempt to resolve the human-readable timezone based on coordinates."""
        tf = TimezoneFinder()
        try:
            tz = tf.timezone_at(lat=float(self.coord.lat), lng=float(self.coord.lon))
            self.timezone_human_readable = tz or "Unknown"
            self.timezone_error = tz is None
        except Exception as e:
            logger.warning(
                f"Failed to resolve timezone for lat={self.coord.lat}, lon={self.coord.lon}: {e}"
            )
            self.timezone_human_readable = "Unknown"
            self.timezone_error = True
        return self


class ErrorWeatherLocationModel(WeatherLocation):
    error: bool = Field(default=True, description="Indicates this is an error response")
    zip_code: str = Field(..., description="ZIP code that caused the error")
    coord: Coord = Field(
        default=Coord(lat=Decimal("9999.0"), lon=Decimal("9999.0")),
        description="Placeholder coordinates for an error case",
    )
    timezone_offset_seconds: int = Field(
        default=0, description="Defaulted timezone offset in seconds for error case"
    )
    timezone_human_readable: str = Field(
        default="Unknown", description="Defaulted timezone string for error case"
    )


class UserResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the created user")


class UserData(BaseModel):
    name: str = Field(..., description="Full name of the user")
    zip_code: str = Field(..., description="ZIP code of the user")
    latitude: str = Field(..., description="Latitude of the user location as string")
    longitude: str = Field(..., description="Longitude of the user location as string")
    timezone_offset_seconds: int = Field(..., description="Timezone offset in seconds")
    timezone: str = Field(..., description="Human-readable timezone string")
    timezone_error: bool = Field(..., description="True if timezone resolution failed")
