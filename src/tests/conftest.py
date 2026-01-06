import os
import pytest, pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session

os.environ["PROFILE"]="test"


from common.database import Base, engine, get_db
from main import app
from .common_test.database.init_test_data import init_test_database
import asyncio

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
        echo=True,
        poolclass=StaticPool
    )
    return engine

@pytest_asyncio.fixture(scope="session")
async def setup_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    Session = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with Session() as db_session:
        await init_test_database(db_session)
        await db_session.commit()

    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest_asyncio.fixture
def session_maker(test_engine):
    return async_sessionmaker(bind=test_engine,
                              expire_on_commit=False,
                              class_=AsyncSession)

@pytest_asyncio.fixture
async def session(session_maker, setup_db):
    async with session_maker() as s:
        yield s

@pytest_asyncio.fixture
async def app_with_test_db(session_maker, setup_db):
    async def override_get_session():
        async with session_maker() as s:
            yield s
    app.dependency_overrides.clear()
    app.dependency_overrides.setdefault(
        get_db,
        override_get_session
    )
    return app

@pytest_asyncio.fixture
async def client(app_with_test_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
