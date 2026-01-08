from pydantic_settings import SettingsConfigDict

from .base_profile_config import BaseProfileConfig

class TestProfileConfig(BaseProfileConfig):
    DATABASE_URL:str

    model_config = SettingsConfigDict(
        env_file=".env.test",
        extra="ignore"
    )