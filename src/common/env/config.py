from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from common.env.profile import PROFILE_CLASS_MAP, BaseProfileConfig

class Settings(BaseSettings):
    PROFILE: str
    DATABASE_URL: str
    profile_config: BaseProfileConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        frozen=True
    )

    def model_post_init(self, __context: Any, /) -> None:
        cls = PROFILE_CLASS_MAP[self.PROFILE]
        object.__setattr__(self, "profile_config", cls())

settings = Settings()
