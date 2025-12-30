from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.base import Base
from app.api import deps
from app.models import user as user_model
from app.core import security

from sqlalchemy.pool import StaticPool

# test database connection (in-memory sqlite)
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    # create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    # drop tables after tests
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    # dependency override
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[deps.get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def test_user_token(client: TestClient, db: Session) -> str:
    email = "testuser@example.com"
    password = "testpassword"
    user_in = user_model.User(
        email=email,
        hashed_password=security.get_password_hash(password)
    )
    db.add(user_in)
    db.commit()
    
    login_data = {
        "username": email,
        "password": password,
    }
    response = client.post("/api/v2/auth/login", data=login_data)
    return response.json()["access_token"]
