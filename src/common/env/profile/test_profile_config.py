from .base_profile_config import BaseProfileConfig

class TestProfileConfig(BaseProfileConfig):
    database_url:str = r"sqlite:///:memory"