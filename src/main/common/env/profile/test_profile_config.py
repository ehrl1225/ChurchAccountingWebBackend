from .base_profile_config import BaseProfileConfig

class TestProfileConfig(BaseProfileConfig):
    DATABASE_URL:str = "sqlite:///:memory:"