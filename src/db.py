import random
from typing import List, Optional, Union, Tuple
from fastapi import Depends, Query
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select, and_
from sqlalchemy import UniqueConstraint

default_schedule = "8,20"


class UserBase(SQLModel):
    __table_args__ = (UniqueConstraint("telegram_chat_id"),)
    name: str
    telegram_chat_id: int
    gmt: Optional[int] = 0
    active: Optional[bool] = True
    scheduled_hours: Optional[str] = default_schedule


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
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)


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
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
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
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
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


def get_user_status(
    telegram_chat_id: int,
    session: Session = next(get_session()),
) -> Optional[Tuple[int, bool]]:
    """
    Get status of the user.

    Args:
        telegram_chat_id:
        session:

    Returns: (gmt,active)

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == telegram_chat_id)
    ).first()
    if found_user is None:
        return None, None
    else:
        return found_user.gmt, found_user.active


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
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    if len(found_user.reminders) > 0:
        memory_list = found_user.reminders
        random_memory = random.choice(memory_list)
        return random_memory
    else:
        return False


def list_memories(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[List[Reminder]]:
    """
    Return all the memory-vault.

    Args:
        user:
        session:

    Returns:

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None

    return found_user.reminders


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
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()

    if found_user is None:
        return None

    else:
        found_memory = session.exec(
            select(Reminder).where(
                and_(Reminder.user == found_user, Reminder.reminder == memory)
            )
        ).first()
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


def delete_memory(
    user: UserCreate,
    memory_id: int,
    session: Session = next(get_session()),
) -> Union[bool, str, None]:
    """
    Delete a memory from user's memory-vault.

    Args:
        user:
        memory_id:
        session:

    Returns: bool

    """

    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    if len(found_user.reminders) > memory_id:
        reminder = found_user.reminders[memory_id]
        memory = reminder.reminder
        session.delete(reminder)
        session.commit()
        return memory
    else:
        return False


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
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    else:
        found_user.gmt = gmt
        session.add(found_user)
        session.commit()
        session.refresh(found_user)
        return found_user


def get_schedule(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[List[int]]:
    """
    Get schedule of the user.

    Args:
        user:
        session:

    Returns: str or None

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    else:
        schedule = found_user.scheduled_hours
        schedule_list = []
        for strnumber in schedule.split(","):
            schedule_list.append(int(strnumber))
        schedule_list.sort()
        return schedule_list


def reset_schedule(
    user: UserCreate,
    session: Session = next(get_session()),
) -> Optional[str]:
    """
    Reset schedule of the user.

    Args:
        user:
        session:

    Returns: str or None

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    else:
        found_user.scheduled_hours = default_schedule
        session.add(found_user)
        session.commit()
        session.refresh(found_user)
        return found_user.scheduled_hours


def remove_hour_from_schedule(
    user: UserCreate,
    hour: str,
    session: Session = next(get_session()),
) -> Optional[str]:
    """
    Remove hour from schedule of the user.

    Args:
        user:
        hour:
        session:

    Returns: str or None

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    else:
        old_schedule = found_user.scheduled_hours
        new_schedule = []
        for str_number in old_schedule.split(","):
            if not hour == str_number:
                new_schedule.append(str_number)
        str_schedule = ",".join(new_schedule)
        found_user.scheduled_hours = str_schedule
        session.add(found_user)
        session.commit()
        session.refresh(found_user)
        return found_user.scheduled_hours


def add_hours_to_the_schedule(
    user: UserCreate,
    schedule_list: List[int],
    session: Session = next(get_session()),
) -> Optional[str]:
    """
    Add hours to the schedule of the user.

    Args:
        user:
        schedule_list:
        session:

    Returns: str or None

    """
    found_user = session.exec(
        select(User).where(User.telegram_chat_id == user.telegram_chat_id)
    ).first()
    if found_user is None:
        return None
    else:
        old_schedule = found_user.scheduled_hours
        new_schedule = []
        for strnumber in old_schedule.split(","):
            new_schedule.append(int(strnumber))
        for strnumber in schedule_list:
            new_schedule.append(strnumber)
        sorted_schedule = sorted(new_schedule)
        str_sorted_schedule = [str(number) for number in sorted_schedule]
        str_schedule = ",".join(str_sorted_schedule)
        found_user.scheduled_hours = str_schedule
        session.add(found_user)
        session.commit()
        session.refresh(found_user)
        return found_user.scheduled_hours


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
    only_active_users: bool = True,
    session: Session = next(get_session()),
    offset: int = 0,
    limit: int = 100,
):
    if only_active_users:
        users = session.exec(select(User).where(User.active).offset(offset).limit(limit)).all()
    else:
        users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users
