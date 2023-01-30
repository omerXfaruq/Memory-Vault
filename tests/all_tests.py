import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from src.listener import app, User, UserCreate, get_session
from src.events import Events
from src.db import *

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
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
async def test_main_event():
    return True
    await Events.main_event()


@pytest.mark.asyncio
def test_time_until_midday():
    print(Events.get_time_until_next_hour())


def test_add_user_to_db(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = db_create_user(user, session=session)
    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    assert user_list[0] == user


def test_user_send_time_list(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = User.from_orm(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    assert user_list[0] == user
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    print(found_user)
    found_user.scheduled_hours = "1,2"
    session.add(found_user)
    session.commit()
    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    assert user_list[0] == user


def test_add_and_remove_users(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = User.from_orm(user)
    db_create_user(user, session)
    add_memory(user, "hey", session)
    add_memory(user, "heyyo", session)
    add_memory(user, "hey", session)
    assert list_memories(user, session) == [
        Reminder(user_id=1, reminder="heyyo", id=2),
        Reminder(user_id=1, reminder="hey", id=3),
    ]


def test_add_schedules(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = User.from_orm(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    assert user_list[0] == user

    scheduled_hours = add_hours_to_the_schedule(user, [1, 13], session)
    split_hours = scheduled_hours.split(",")
    str_set1 = set()
    for str in split_hours:
        str_set1.add(str)
    str_set2 = set()
    str_set2.add("20")
    str_set2.add("1")
    str_set2.add("13")
    str_set2.add("8")

    assert str_set2 == str_set1

    user_list = db_read_users(session=session)
    assert 1 == len(user_list)
    print(user_list[0])


def test_db_read_users(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = db_create_user(user, session=session)
    user2 = UserCreate(
        name="22lloll",
        telegram_chat_id=12200100010001,
    )
    user2.active = False
    user2 = db_create_user(user2, session=session)

    user_list = db_read_users(session=session, only_active_users=False, limit=1)
    assert 1 == len(user_list)
    assert user_list[0] == user
    print(user_list)


def test_read_random_user(session):
    user = UserCreate(
        name="lloll",
        telegram_chat_id=100100010001,
    )
    user = db_create_user(user, session=session)
    user2 = UserCreate(
        name="22lloll",
        telegram_chat_id=12200100010001,
    )
    user2.active = False
    user2 = db_create_user(user2, session=session)

    from sqlalchemy import func

    random_user = session.exec(select(User).order_by(func.random()).limit(2)).all()
    print(random_user)
    assert False


def test_print_start_message():
    name = ""
    language_code = "en"
    from src.constants import Constants

    print()
    print(Constants.Start.start_message(name, language_code))


def test_print_help_message():
    name = ""
    language_code = "en"
    from src.constants import Constants

    print()
    print(Constants.Help.help_message(name, language_code))
