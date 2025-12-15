from .base_profile_config import BaseProfileConfig

class DevProfileConfig(BaseProfileConfig):
    DATABASE_URL:str = r"sqlite:///./db.sqlite3"