from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from TodoApp.database import Base
from TodoApp.main import app
from fastapi.testclient import TestClient
import pytest
from TodoApp.models import Todos,Users
from TodoApp.routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db ## return all info then run finally clause
    finally:
        db.close()

def override_get_current_user():
    return {'username':'codingwithrobytest','id':1,'user_role':'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
    id=1,
    email = "codingwithrobytest@email.com",
    username = "codingwithrobytest",
    first_name = "Eric",
    last_name = "Roby",
    hashed_password = bcrypt_context.hash("testpassword"),
    is_active = True,
    role = "admin",
    phone_number = "0123456789"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()