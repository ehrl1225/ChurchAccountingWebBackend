from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from common.env.profile import PROFILE_CLASS_MAP, BaseProfileConfig

class Settings(BaseSettings):
    PROFILE: str
    profile_config: BaseProfileConfig | None = None
    SECRET_KEY: str
    SMTP_PASS: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    SERVER_PEPPER: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    REGION_NAME: str
    BUCKET_NAME: str


    model_config = SettingsConfigDict(
        env_file=".env",
    )

    def model_post_init(self, __context: Any, /) -> None:
        cls = PROFILE_CLASS_MAP[self.PROFILE]
        object.__setattr__(self, "profile_config", cls())

settings = Settings()