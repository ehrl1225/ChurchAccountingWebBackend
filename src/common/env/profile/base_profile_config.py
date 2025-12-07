from pydantic_settings import BaseSettings

class BaseProfileConfig(BaseSettings):
    DATABASE_URL: str = r"sqlite:///:./db.sqlite3"
    VERIFY_TOKEN_EXPIRATION: int =  60 * 60 * 24
    SERVER_BASE_URL: str = r"http://localhost:8000"
    SMTP_HOST = r"smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "ehrl0506@gmail.com"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7