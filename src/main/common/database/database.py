from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from common.env import settings
from fastapi import Request

engine = create_async_engine(settings.profile_config.get_database_url())

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

def get_db(request: Request) -> AsyncSession:
    return request.state.db