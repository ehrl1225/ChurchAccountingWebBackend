from .base_profile_config import BaseProfileConfig

class DevProfileConfig(BaseProfileConfig):
    database_url:str = r"sqlite:///:memory"