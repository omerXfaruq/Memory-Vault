import asyncio
import datetime

from fastapi import FastAPI, Depends
from .db import *
from .message_validations import MessageBodyModel, ResponseToMessage
from .constants import Constants
from .events import Events
from .response_logic import ResponseLogic

app = FastAPI(openapi_url=None)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    asyncio.create_task(Events.main_event())


@app.get("/health")
async def health():
    return {"healthy": True}


@app.post(f"/webhook/{Events.TOKEN}")
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


@app.post(f"/trigger_send_user_hourly_memories/{Events.TOKEN}")
async def trigger_send_user_hourly_memories(*, session: Session = Depends(get_session)):
    users = db_read_users(limit=100000, session=session)
    now = datetime.datetime.now()
    print(f"Sending is triggered at hour {now.hour}, GMT:{Events.CURRENT_TIMEZONE}")
    for user in users:
        Events.send_user_hourly_memories(user, now.hour)
