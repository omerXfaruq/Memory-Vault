from .db import UserCreate, join_user, leave_user, select_random_memory, add_memory, delete_memory, list_memories, update_gmt, get_user_status
from .events import Events
from .constants import Constants


class ResponseLogic:
    @staticmethod
    async def create_response(text: str, name: str, chat_id: int) -> str:

        split_text = text.split(" ")
        first_word = split_text[0].lower()
        user = UserCreate(
            name=name,
            telegram_chat_id=chat_id,
        )

        if first_word == "/start":
            response_message = Constants.start_message(name)
        elif first_word == "help" or first_word == "/help":
            response_message = Constants.HELP_MESSAGE
        elif first_word == "join" or first_word == "/join":
            user = join_user(user)

            if user is not None and user.telegram_chat_id == chat_id:
                response_message = f"Welcome onboard {name}, you joined into my system. I will send you a random memory at every midday from your memory vault. You can get more detailed information by writing, *help*."
            else:
                response_message = f"You are already in the system."

        elif first_word == "leave" or first_word == "/leave":
            user = leave_user(user)
            if user is not None and user.telegram_chat_id == chat_id:
                response_message = f"Good bye {name}, I deactivated you in my system. It was nice to have you here. Your memory vault remains with me, you can return whenever you wish with command, *join*."
            else:
                response_message = f"Your account was already inactive."

        elif first_word == "send" or first_word == "/send":
            memory = select_random_memory(user)
            if memory is None:
                response_message = (
                    "The user is not in the system, please join by typing; *join*."
                )
            elif memory is False:
                response_message = "No memory found in the system. Please add memory, for further information you can type *help*."
            else:
                response_message = memory.reminder

        elif first_word == "list" or first_word == "/list":
            memories = list_memories(user)
            if memories is None:
                response_message = (
                    "The user is not in the system, please join by typing; *join*."
                )
            elif len(memories) == 0:
                response_message = "No memory found in the system. Please add memory, for further information you can type *help*."
            else:
                # TODO: send in batches of 10 messages
                response_message = (
                    f"Open the gates of the memory vault!"
                    f"\n*id | memory*"
                )

                for id, reminder in enumerate(memories):
                    response_message += f"\n{id}: {reminder.reminder}"
                response_message

        elif first_word == "add" or first_word == "/add":
            memory = " ".join(split_text[1:])
            if str.isspace(memory) or memory == "":
                response_message = f"There is no sentence found after the word *add*.{Constants.HELP_MESSAGE}"
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
        elif first_word == "delete" or first_word == "/delete":
            if len(split_text) < 2:
                response_message = f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."
            else:
                try:
                    memory_id = int(split_text[1])
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

        elif first_word == "schedule" or first_word == "/schedule":
            if len(split_text) == 1:
                # TODO: return current schedule
                raise NotImplementedError
            else:
                if split_text[1] == "reset":
                    raise NotImplementedError
                elif split_text[1] == "add":
                    strnumbers = []
                    number_check = True
                    try:
                        for strnumber in split_text[2:]:
                            number = int(strnumber)
                            strnumbers.append(number)
                            if not (0 <= number <= 23):
                                number_check = False
                                break
                    except:
                        response_message = f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21"
                    if not number_check:
                        response_message = f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21"
                    else:
                        if str.isspace(strnumbers) or strnumbers == "":
                            response_message = f"There is no numbers found *schedule add*.{Constants.HELP_MESSAGE}"

                elif split_text[1] == "remove":
                    raise NotImplementedError

        elif first_word == "gmt" or first_word == "/gmt":
            try:
                gmt = int(split_text[1])
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

        elif first_word == "broadcast" or first_word == "/broadcast":
            if chat_id == Constants.BROADCAST_CHAT_ID:
                normalized_text = " ".join(split_text[1:])
                if str.isspace(normalized_text) or normalized_text == "":
                    response_message = f"There is no sentence found after the word *broadcast*."
                else:
                    await Events.broadcast_message(normalized_text)
                    response_message = "Broadcast is sent"
            else:
                response_message = "You have no broadcast right"
        elif first_word == "status" or first_word == "/status":
            gmt, active = get_user_status(chat_id)
            if gmt is None:
                response_message = "You have not joined the system yet, please type, *join*."
            else:
                response_message = (
                    f"Your current status:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Daily sending is active: *{active}*"
                )
        elif first_word == "feedback" or first_word == "/feedback":

            message = " ".join(split_text[1:])
            message_with_user_information = message + f"\nFrom the user: *{name}* \nchat id: *{chat_id}*"

            if str.isspace(message) or message == "":
                response_message = f"There is no message found after the word *feedback*."
            else:
                success = await Events.send_a_message_to_user(Constants.FEEDBACK_FORWARD_CHAT_ID, message_with_user_information)
                if success:
                    response_message = f"I forwarded your feedback to the admin, thank you for your support.\nFeedback: *{message}*"
                else:
                    response_message = f"I could not forward your feedback to the admin, an error occurred."

        elif first_word == "support" or first_word == "/support":
            response_message = (f"Thank you, to support me you can"
                                f"\n- Share me with your friends"
                                f"\n- Give feedback using the command, *feedback sentence*"
                                f"\n- Star the github repository at https://github.com/FarukOzderim/Memory-Vault/"
                                )
        else:
            response_message = (
                f"{name}, I do not know that command.{Constants.HELP_MESSAGE}"
            )
        return response_message
