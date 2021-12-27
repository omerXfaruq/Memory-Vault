import asyncio

from fastapi import FastAPI

from .db import *
from .message_validations import MessageBodyModel, ResponseToMessage
from .constants import Constants
from .events import Events

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

    splitted_text = text.split(" ")
    first_word = splitted_text[0].lower()
    user = UserCreate(
        name=name,
        telegram_chat_id=chat_id,
    )

    if first_word == "/start":
        response_message = Constants.start_message(name)
    elif first_word == "help":
        response_message = Constants.HELP_MESSAGE
    elif first_word == "join":
        user = join_user(user)

        if user is not None and user.telegram_chat_id == chat_id:
            response_message = f"Welcome onboard {name}, you joined into my system. I will send you a random memory at every midday from your memory vault. You can get more detailed information by writing, *help*."
        else:
            response_message = f"You are already in the system."

    elif first_word == "leave":
        user = leave_user(user)
        if user is not None and user.telegram_chat_id == chat_id:
            response_message = f"Good bye {name}, I deactivated you in my system. It was nice to have you here. Your memory vault remains with me, you can return whenever you wish with command, *join*."
        else:
            response_message = f"Your account was already inactive."

    elif first_word == "send":
        memory = select_random_memory(user)
        if memory is None:
            response_message = (
                "The user is not in the system, please join by typing; *join*."
            )
        elif memory is False:
            response_message = "No memory found in the system. Please add memory, for further information you can type *help*."
        else:
            response_message = memory.reminder

    elif first_word == "list":
        response = list_memories(user)
        if response is None:
            response_message = (
                "The user is not in the system, please join by typing; *join*."
            )
        elif response is False:
            response_message = "No memory found in the system. Please add memory, for further information you can type *help*."
        else:
            response_message = response

    elif first_word == "add":
        memory = " ".join(splitted_text[1:])
        if str.isspace(memory) or memory == "":
            response_message = f"There is no memory found after the word *add*.\n\n{Constants.HELP_MESSAGE}"
        else:
            reminder = add_memory(user, memory)
            if reminder is None:
                response_message = (
                    "The user is not in the system, please join by typing; *join*."
                )
            elif reminder is False:
                response_message = "The memory is already in your memory vault"
            else:
                memory = reminder.reminder
                response_message = (
                    f"Your memory is added to your memory vault. No worries, I will keep it safe :)."
                    f"\nMemory: {memory}"
                )
    elif first_word == "delete":
        if len(splitted_text) < 2:
            response_message = f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."
        else:
            try:
                memory_id = int(splitted_text[1])
                if memory_id < 0:
                    response_message = f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."
                else:
                    response = delete_memory(user, memory_id)
                    if response is None:
                        response_message = "The user is not in the system, please join by typing; *join*."
                    elif response is False:
                        response_message = "There is no memory with that id, you can list memory ids by using command, *list*."
                    else:
                        memory = response

                        response_message = (
                            f"Your memory is deleted from your memory vault. Good bye to the forgotten memory :("
                            f"\nMemory: {memory}"
                        )

            except Exception as ex:
                response_message = f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."

    elif first_word == "gmt":
        try:
            gmt = int(splitted_text[1])
            if -12 <= gmt <= 12:
                user = update_gmt(user, gmt)
                response_message = f"Your timezone is set to GMT{user.gmt}"

            else:
                response_message = (
                    f"Please give your timezone correctly \n {Constants.HELP_MESSAGE}"
                )

        except Exception as ex:
            response_message = (
                f"Please give your timezone correctly \n {Constants.HELP_MESSAGE}"
            )

    elif first_word == "broadcast":
        if chat_id == Constants.BROADCAST_CHAT_ID:
            normalized_text = " ".join(splitted_text[1:])
            if str.isspace(normalized_text) or normalized_text == "":
                response_message = f"There is no memory found after the word *add*.\n\n{Constants.HELP_MESSAGE}"
            else:
                await Events.broadcast_message(normalized_text)
                response_message = "Broadcast is sent"
        else:
            response_message = "You have no broadcast right"
    elif first_word == "status":
        gmt, active = get_user_status(chat_id)
        if gmt is None:
            response_message = "You have not joined the system yet, please type, *join*."
        else:
            response_message = (
                f"Your current status:"
                f"\n- Gmt: *GMT{gmt}*"
                f"\n- Daily sending is active: *{active}*"
            )
    else:
        response_message = (
            f"{name}, I do not know that command.{Constants.HELP_MESSAGE}"
        )
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
