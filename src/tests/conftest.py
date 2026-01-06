import asyncio
import os

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

os.environ["PROFILE"] = "test"

from main import app
from common.database import Base, get_db
from common.env import settings

# 1. 비동기 테스트 엔진 생성
test_engine = create_async_engine(settings.profile_config.DATABASE_URL)
TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


@pytest.fixture(scope="session")
def event_loop():
    """pytest-asyncio를 위한 이벤트 루프 설정"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """
    세션 당 한 번 테스트 데이터베이스 테이블을 생성하고 삭제합니다.
    """
    # 테이블 생성
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 테스트 데이터 초기화
    # init_test_database가 비동기 함수라고 가정합니다.
    from .common_test.database.init_test_data import init_test_database
    async with TestSessionLocal() as session:
        await init_test_database(session)
        await session.commit()

    yield

    # 테이블 삭제
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client() -> AsyncClient:
    """
    각 테스트 함수를 위한 비동기 클라이언트를 제공합니다.
    모든 테스트는 롤백되는 트랜잭션 안에서 실행됩니다.
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()

    try:
        # 트랜잭션 범위의 세션 생성
        async_session = TestSessionLocal(bind=connection)

        # get_db 의존성 오버라이드
        async def override_get_db() -> AsyncSession:
            yield async_session

        app.dependency_overrides[get_db] = override_get_db

        # 비동기 클라이언트 제공
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

    finally:
        # 테스트 후 정리
        await async_session.close()
        await transaction.rollback()
        await connection.close()
        del app.dependency_overrides[get_db]