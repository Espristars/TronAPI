import os
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from models import Base
from main import app, get_db

db_fd, db_path = tempfile.mkstemp()
SQLALCHEMY_DATABASE_URL = "sqlite:///" + db_path

engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

Base.metadata.create_all(bind=engine_test)


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
    os.unlink(db_path)
