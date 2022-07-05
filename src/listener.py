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
        language_code = message.message.from_field.language_code
        if not text:  # Edit of message  etc.
            return
        else:
            response_message = await ResponseLogic.create_response(
                text, name, chat_id, language_code
            )
            return ResponseToMessage(
                **{
                    "text": response_message,
                    "chat_id": chat_id,
                }
            )

    if not message.message:  # Bot is added to a group
        if not message.my_chat_member:
            return

        chat_id = message.my_chat_member.chat.id
        name = message.my_chat_member.from_field.first_name
        language_code = message.my_chat_member.from_field.language_code

        new_member = message.my_chat_member.new_chat_member
        if (
            new_member
            and new_member.user.id == Constants.BOT_ID
            and new_member.status == "member"
        ):
            await Events.send_a_message_to_user(chat_id, Constants.hello)
            response_message = Constants.Start.start_message(name, language_code)
            return ResponseToMessage(
                **{
                    "text": response_message,
                    "chat_id": chat_id,
                }
            )

    return


@app.post(f"/trigger_send_user_hourly_memories/{Events.TOKEN}")
async def trigger_send_user_hourly_memories(*, session: Session = Depends(get_session)):
    users = db_read_users(limit=100000, session=session)
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"Sending is triggered at hour {now.hour}, GMT:{Events.CURRENT_TIMEZONE}")
    for user in users:
        Events.send_user_hourly_memories(user, now.hour)
