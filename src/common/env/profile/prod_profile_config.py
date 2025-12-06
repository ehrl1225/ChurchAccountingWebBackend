from .base_profile_config import BaseProfileConfig

class ProdProfileConfig(BaseProfileConfig):
    database_url:str = r"sqlite:///:memory"