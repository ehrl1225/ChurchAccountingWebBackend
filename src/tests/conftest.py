import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ["PROFILE"]="test"


from common.database import Base, engine, get_db
from main import app
from .common.database.init_test_data import init_test_database
import asyncio

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Creates all tables in the test database once per session.
    :return:
    """

    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    session = Session(bind=connection)
    asyncio.run(init_test_database(session))
    session.commit()
    connection.close()

    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Session:
    """
    Provides a transactional database session for each test function.
    Rolls back the transaction after the test, ensuring isolation.
    :return:
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """
    Provides a FastAPI TestClient that is configured to use the transactional db_session
    :param db_session:
    :return:
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

