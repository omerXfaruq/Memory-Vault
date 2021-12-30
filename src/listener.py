import asyncio

from fastapi import FastAPI

from .db import *
from .message_validations import MessageBodyModel, ResponseToMessage
from .constants import Constants
from .events import Events
from .response_logic import ResponseLogic

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    asyncio.create_task(Events.main_event())


@app.post("/webhook/{secret}")
async def listen_telegram_messages(message: MessageBodyModel):
    print(message.dict())
    if message.message:
        name = message.message.from_field.first_name
        chat_id = message.message.chat.id
        text = message.message.text
        if text is None:  # Bot is given admin rights or added to the group
            return ResponseToMessage(
                **{
                    "text": Constants.start_message(name),
                    "chat_id": chat_id,
                }
            )
    else:  # A message is edited
        return

    response_message = await ResponseLogic.create_response(text, name, chat_id)
    return ResponseToMessage(
        **{
            "text": response_message,
            "chat_id": chat_id,
        }
    )


@app.post("/user/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    user = User.from_orm(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.post("/reminder/", response_model=ReminderRead)
def create_reminder(
    *, session: Session = Depends(get_session), reminder: ReminderCreate
):
    db_reminder = Reminder.from_orm(reminder)
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder


@app.get("/reminders/", response_model=List[ReminderRead])
def read_reminders(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    reminders = session.exec(select(Reminder).offset(offset).limit(limit)).all()
    return reminders
