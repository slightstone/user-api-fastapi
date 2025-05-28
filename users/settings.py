from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    openweathermap_api_key: str = Field(..., alias="OPENWEATHERMAP_API_KEY")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
