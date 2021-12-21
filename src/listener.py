import sys

from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
import uvicorn
import asyncio
from pyngrok import ngrok

from db import *
from events import Events
from message_validations import MessageBodyModel, ResponseToMessage

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/webhook/{secret}")
async def listen_telegram_messages(message: MessageBodyModel):
    name = message.message.chat.first_name
    text = message.message.text

    help_message = (
        f"\n\nThis bot will send you a random memory at every midday from your memory vault. "
        f"\n\n- You can join my system by writing, join."
        f"\n- You can add memories to your memory vault with command,  add Sentence."
        f"\nExample:"
        f"\nadd Time does not come back."

        f"\n\n- You can set your timezone with command, \"gmt timezone\". Default timezone is GMT0."
        f"\nExamples:"
        f"\n. GMT+3: gmt 3"
        f"\n. GMT0: gmt 0"
        f"\n. GMT-5: gmt -5"
    )
    splitted_text = text.split(" ")
    first_word = splitted_text[0]
    if first_word == "/start":
        response_message = (
            f"Welcome onboard {name}, This bot will send you a random memory at every midday from your memory vault. "
            f"\n- You can join my system by writing, join. "
            f"\n- You can get more detailed information by writing help."
        )
    elif first_word == "help":
        response_message = help_message

    elif first_word == "leave":
        response_message = (
            f"Good bye {name}, I deleted you from my system. It was nice to have you here. Your memory vault remains with me, you can return whenever you wish with command, join."
        )
    elif first_word == "add":
        response_message = (
            f"Your memory is added to your memory vault. No worries, I will keep it safe :)."
        )

    else:
        response_message = f"{name}, I do not know that command.{help_message}"

    return ResponseToMessage(
        **{
            "text": response_message,
            "chat_id": message.message.chat.id,
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
def create_reminder(*, session: Session = Depends(get_session), reminder: ReminderCreate):
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


if __name__ == '__main__':
    if Events.TOKEN is None:
        sys.exit("No TELEGRAM_TOKEN found in the environment, exiting now.")
    PORT = 8000
    http_tunnel = ngrok.connect(PORT, bind_tls=True)
    public_url = http_tunnel.public_url
    Events.HOST_URL = public_url

    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(Events.set_telegram_webhook_url())
    if success:
        uvicorn.run("listener:app", host="127.0.0.1", port=PORT, log_level="info")
    else:
        print("Fail, closing the app.")
