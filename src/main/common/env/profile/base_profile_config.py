from pydantic_settings import BaseSettings

class BaseProfileConfig(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    VERIFY_TOKEN_EXPIRATION: int =  60 * 60 * 24
    SERVER_BASE_URL: str = r"http://localhost:8000"
    SMTP_HOST: str = r"smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "ehrl0506@gmail.com"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REDIS_HOST: str = "localhost"
    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def get_database_url(self):
        return self.DATABASE_URL