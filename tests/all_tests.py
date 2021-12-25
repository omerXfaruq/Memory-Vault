import pytest
import asyncio

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.listener import app, User, UserCreate, get_session
from src.events import Events
from src.db import db_create_user, db_read_users, Reminder

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_send_message():
    response = await Events.single_user_mail(1, 861126057, 0, [Reminder(reminder="salam")])
    assert response


@pytest.mark.asyncio
async def test_main_event():
    return
    await Events.main_event()


@pytest.mark.asyncio
def test_time_until_midday():
    print(Events.get_time_until_midday())


def test_add_user_to_db(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = db_create_user(user, session=session)
    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    assert user_list[0] == user
