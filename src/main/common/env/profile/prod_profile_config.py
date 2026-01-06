from .base_profile_config import BaseProfileConfig

class ProdProfileConfig(BaseProfileConfig):
    DATABASE_URL:str = r"sqlite+aiosqlite:///:memory:"