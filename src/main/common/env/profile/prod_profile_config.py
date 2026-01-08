from pydantic_settings import SettingsConfigDict

from .base_profile_config import BaseProfileConfig

class ProdProfileConfig(BaseProfileConfig):
    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env.prod",
        extra="ignore",
    )

    def get_database_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"