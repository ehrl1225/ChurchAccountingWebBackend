from pydantic_settings import BaseSettings

class BaseProfileConfig(BaseSettings):
    database_url: str
