import random
from typing import List, Optional, Union
from fastapi import Depends, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, and_
from sqlalchemy import UniqueConstraint


class UserBase(SQLModel):
    __table_args__ = (UniqueConstraint("telegram_chat_id"),)
    name: str
    telegram_chat_id: int
    gmt: Optional[int] = 0
    active: Optional[bool] = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reminders: List["Reminder"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class ReminderBase(SQLModel):
    reminder: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Reminder(ReminderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="reminders")


class ReminderRead(ReminderBase):
    id: int


class ReminderCreate(ReminderBase):
    pass


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def join_user(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[User]:
    """
    Joins the user to the system.

    Args:
        user:
        session:

    Returns: User or None

    """
    found_user = session.exec(select(User).where(User.telegram_chat_id == user.telegram_chat_id)).first()
    if found_user is None:
        user = db_create_user(user, session)
        return user
    else:
        if found_user.active:
            return None
        else:
            found_user.active = True
            session.add(found_user)
            session.commit()
            session.refresh(found_user)
            return found_user


def leave_user(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[User]:
    """
    Deactivates the user.

    Args:
        user:
        session:

    Returns: User or None

    """
    found_user = session.exec(select(User).where(User.telegram_chat_id == user.telegram_chat_id)).first()
    if found_user is None:
        return None
    else:
        if not found_user.active:
            return None
        else:
            found_user.active = False
            session.add(found_user)
            session.commit()
            session.refresh(found_user)
            return found_user


def select_random_memory(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[Union[Reminder, bool]]:
    """
    Select random memory from user's memory-vault.

    Args:
        user:
        session:

    Returns:

    """
    found_user = session.exec(select(User).where(User.telegram_chat_id == user.telegram_chat_id)).first()
    if found_user is None:
        return None
    if len(found_user.reminders) > 0:
        memory_list = found_user.reminders
        random_memory = random.choice(memory_list)
        return random_memory
    else:
        return False


def add_memory(
    user: UserCreate,
    memory: str,
    session: Session = next(get_session()),
) -> Optional[Union[Reminder, bool]]:
    """
    Add a memory to user's memory-vault.

    Args:
        user:
        memory:
        session:

    Returns: Reminder

    """
    found_user = session.exec(select(User).where(User.telegram_chat_id == user.telegram_chat_id)).first()

    if found_user is None:
        return None

    else:
        found_memory = session.exec(select(Reminder).where(and_(Reminder.user == found_user, Reminder.reminder == memory))).first()
        if found_memory is not None:
            print(f"Found: {found_memory}")
            return False
        else:
            reminder = ReminderCreate(
                reminder=memory,
                user_id=found_user.id,
            )

            db_reminder = Reminder.from_orm(reminder)
            session.add(db_reminder)
            session.commit()
            session.refresh(db_reminder)
            return db_reminder


def update_gmt(
    user: UserCreate,
    gmt: int,
    session: Session = next(get_session()),
) -> Optional[User]:
    """
    Update GMT of the user.

    Args:
        user:
        session:

    Returns: User or None

    """
    found_user = session.exec(select(User).where(User.telegram_chat_id == user.telegram_chat_id)).first()
    if found_user is None:
        return None
    else:
        found_user.gmt = gmt
        session.add(found_user)
        session.commit()
        session.refresh(found_user)
        return found_user


def db_create_user(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[User]:
    try:
        user = User.from_orm(user)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    except Exception as ex:
        return None


def db_read_users(
    *,
    session: Session = next(get_session()),
    offset: int = 0,
    limit: int = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


def create_reminder(*, session: Session = Depends(get_session), reminder: ReminderCreate):
    db_reminder = Reminder.from_orm(reminder)
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder


def read_reminders(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    reminders = session.exec(select(Reminder).offset(offset).limit(limit)).all()
    return reminders
