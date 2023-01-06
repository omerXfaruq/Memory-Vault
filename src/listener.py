import asyncio
import datetime

from fastapi import FastAPI, Depends, Request
from fastapi.concurrency import run_in_threadpool
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
async def listen_telegram_messages(r: Request, message: MessageBodyModel):
    print(f"%% {datetime.datetime.now()} Incoming Message: {message.dict()}")
    print(f"%% {datetime.datetime.now()} Incoming Request: {await r.json()}")

    response_message = None

    if message.message:
        name = message.message.from_field.first_name
        chat_id = message.message.chat.id
        language_code = message.message.from_field.language_code

        if message.message.photo:
            photo_id = message.message.photo[-1].file_id
            response_message = await ResponseLogic.create_response(
                f"add photo: {photo_id}", name, chat_id, language_code
            )
        elif message.message.document:
            document_id = message.message.document.file_id
            response_message = await ResponseLogic.create_response(
                f"add document: {document_id}", name, chat_id, language_code
            )
        elif message.message.video:
            document_id = message.message.video.file_id
            response_message = await ResponseLogic.create_response(
                f"add document: {document_id}", name, chat_id, language_code
            )
        elif message.message.video_note:
            document_id = message.message.video_note.file_id
            response_message = await ResponseLogic.create_response(
                f"add document: {document_id}", name, chat_id, language_code
            )
        elif message.message.voice:
            document_id = message.message.voice.file_id
            response_message = await ResponseLogic.create_response(
                f"add document: {document_id}", name, chat_id, language_code
            )
        elif message.message.forward_date:
            if message.message.text:
                response_message = await ResponseLogic.create_response(
                    f"add {message.message.text}", name, chat_id, language_code
                )
        elif message.message.text:
            response_message = await ResponseLogic.create_response(
                message.message.text, name, chat_id, language_code
            )
        else:
            return

    elif not message.message:  # Bot is added to a group
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
            start_message = await ResponseLogic.create_response(
                "start", name, chat_id, language_code
            )
            await Events.send_a_message_to_user(chat_id, start_message)
            response_message = Constants.Start.group_warning(name, language_code)

    return ResponseToMessage(
        **{
            "text": response_message,
            "chat_id": chat_id,
        }
    )


@app.post(f"/trigger_archive_db/{Events.TOKEN}")
def trigger_archive_db():
    Events.archive_db()


@app.post(f"/trigger_send_user_hourly_memories/{Events.TOKEN}")
async def trigger_send_user_hourly_memories(*, session: Session = Depends(get_session)):
    users = db_read_users(limit=100000, session=session)
    now = datetime.datetime.now(datetime.timezone.utc)
    for user in users:
        Events.send_user_hourly_memories(user, now.hour)
