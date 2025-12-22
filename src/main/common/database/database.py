from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from common.env import settings
from fastapi import Request

engine = create_engine(settings.profile_config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db(request: Request):
    return request.state.db