import os
import tempfile
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
from main import app, get_db
import asyncio

db_fd, db_path = tempfile.mkstemp()
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/db"

engine_test = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def create_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_db())


@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    os.close(db_fd)
