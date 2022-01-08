import random
import asyncio

from .db import (
    UserCreate, join_user, leave_user, select_random_memory, add_memory, delete_memory, list_memories, update_gmt, get_user_status, get_schedule, reset_schedule, add_hours_to_the_schedule, remove_hour_from_schedule,
    default_schedule)
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
            await Events.send_a_message_to_user(chat_id, Constants.hello)
            return Constants.start_message(name)
        elif first_word == "help" or first_word == "/help":
            return Constants.HELP_MESSAGE
        elif first_word == "join" or first_word == "/join":
            user = join_user(user)

            if user is not None:
                return (
                    f"Welcome onboard {name}, you activated daily memory sending. I will send you random memories from your memory vault according to your schedule."
                    f"The default schedule hours are {default_schedule}. You can get more detailed information by writing, *help* or */help*."
                )
            else:
                return f"Your account is already active."

        elif first_word == "leave" or first_word == "/leave":
            user = leave_user(user)
            if user is not None and user.telegram_chat_id == chat_id:
                return f"Good bye {name}, you deactivated daily memory sending. It was nice to have you here. Your memory vault remains with me, you can return whenever you wish with command, join or */join*."
            else:
                return f"Your account was already inactive."

        elif first_word == "send" or first_word == "/send":
            if len(split_text) == 1:
                memory = select_random_memory(user)
                if memory is None:
                    return (
                        "The user is not in the system, please join by typing; *join* or /join"
                    )
                elif memory is False:
                    return "No memory found in the system. Please add memory, for further information you can type *help* or /help"
                else:
                    return memory.reminder
            else:
                try:
                    number_of_sending = int(split_text[1])
                    if not (1 <= number_of_sending < 50):
                        return "Please give a number which is 1<n<50  after *send*"
                except:
                    return "Please give a number which is 1<n<50  after *send*"

                all_memories = list_memories(user)
                number_of_sending = min(len(all_memories), number_of_sending)
                selected_memories = random.sample(all_memories, number_of_sending)
                for memory in selected_memories:  # Send the memories in background
                    asyncio.create_task(Events.send_a_message_to_user(user.telegram_chat_id, memory.reminder))
                return ""

        elif first_word == "list" or first_word == "/list":
            memories = list_memories(user)
            if memories is None:
                return (
                    "The user is not in the system, please join by typing; join or */join*."
                )
            elif len(memories) == 0:
                return "No memory found in the system. Please add memory, for further information you can type help or */help*."
            else:
                response_message = (
                    f"Brace yourself, you will receive a message every second."
                    f"\nOpen the gates of the memory vault!"
                    f"\n*id | memory*"
                )

                for message_id, reminder in enumerate(memories):
                    message = f"\n{message_id}: {reminder.reminder}"
                    asyncio.create_task(Events.send_a_message_to_user(telegram_id=chat_id, message=message, sleep_time=(message_id + 1)))
                return response_message

        elif first_word == "add" or first_word == "/add":
            memory = " ".join(split_text[1:])
            if str.isspace(memory) or memory == "":
                return f"There is no sentence found after the word *add*.{Constants.HELP_MESSAGE}"
            else:
                reminder = add_memory(user, memory)
                if reminder is None:
                    return (
                        "The user is not in the system, please join by typing; *join*."
                    )
                elif reminder is False:
                    return "The memory is already in your memory vault"
                else:
                    memory = reminder.reminder
                    return (
                        f"Your memory is added to your memory vault. No worries, I will keep it safe :)."
                        f"\nMemory: {memory}"
                    )
        elif first_word == "delete" or first_word == "/delete":
            if len(split_text) < 2:
                return f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."
            else:
                try:
                    memory_id = int(split_text[1])
                    if memory_id < 0:
                        return f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."
                    else:
                        response = delete_memory(user, memory_id)
                        if response is None:
                            return "The user is not in the system, please join by typing; *join*."
                        elif response is False:
                            return "There is no memory with that id, you can list memory ids by using command, *list*."
                        else:
                            memory = response

                            return (
                                f"Your memory is deleted from your memory vault. Good bye to the forgotten memory :("
                                f"\nMemory: {memory}"
                            )

                except Exception as ex:
                    return f"You need to give me id of the memory, ie: *delete 2*, you can get it by using command, *list*."

        elif first_word == "schedule" or first_word == "/schedule":
            if len(split_text) == 1:
                schedule = get_schedule(user)
                if schedule is None:
                    return f"You are not in the system, please join by, */join*."
                else:
                    return (
                        f"*Schedule*:"
                        f"\n{schedule}"
                        f"\nYou will get a random memory at each of these hours everyday."
                    )

            elif len(split_text) > 1:
                if split_text[1] == "reset":
                    new_schedule = reset_schedule(user)
                    if new_schedule is None:
                        return f"You are not in the system, please join by, */join*."
                    else:
                        return (
                            f"*Your New Schedule*:"
                            f"\n{new_schedule}"
                            f"\nYou will get a random memory at each of these hours everyday."
                        )

                elif split_text[1] == "add":
                    str_numbers = []
                    preceding_text = " ".join(split_text[2:])
                    if str.isspace(preceding_text) or preceding_text == "":
                        return f"There is no numbers found after *schedule add*, usage example: *schedule add 1 3 5 21*"

                    number_check = True
                    try:
                        for str_number in split_text[2:]:
                            number = int(str_number)
                            str_numbers.append(number)
                            if not (0 <= number <= 23):
                                number_check = False
                                break
                    except:
                        return f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21*"

                    if not number_check:
                        return f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21*"
                    else:
                        new_schedule = add_hours_to_the_schedule(user, str_numbers)
                        if new_schedule is None:
                            return f"You are not in the system, please join by, */join*."
                        else:
                            return (
                                f"*Your New Schedule*:"
                                f"\n{new_schedule}"
                                f"\nYou will get a random memory at each of these hours everyday."
                            )
                elif split_text[1] == "remove":
                    preceding_text = " ".join(split_text[2:])
                    number_check = True
                    if str.isspace(preceding_text) or preceding_text == "":
                        return f"There is no numbers found after *schedule add*, usage example: *schedule add 1 3 5 21*"
                    else:
                        try:
                            str_number = split_text[2]
                            number = int(str_number)
                            if not (0 <= number <= 23):
                                number_check = False
                        except:
                            return f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21*"

                        if not number_check:
                            return f"Please use numbers 0<=number<=23, ie. *schedule add 1 3 5 21*"
                        else:
                            new_schedule = remove_hour_from_schedule(user, str_number)
                            if new_schedule is None:
                                return f"You are not in the system, please join by, */join*."
                            else:
                                return (
                                    f"*Your New Schedule*:"
                                    f"\n{new_schedule}"
                                    f"\nYou will get a random memory at each of these hours everyday."
                                )

                else:
                    return (
                        f"{name}, I do not know that command. I only support below commands about schedule"
                        f"\n*schedule*"
                        f"\n*schedule add*"
                        f"\n*schedule reset*"
                        f"\n*schedule remove*"

                    )

        elif first_word == "gmt" or first_word == "/gmt":
            try:
                gmt = int(split_text[1])
                if -12 <= gmt <= 12:
                    user = update_gmt(user, gmt)
                    return f"Your timezone is set to GMT{user.gmt}"

                else:
                    return (
                        f"Please give your timezone correctly \n {Constants.HELP_MESSAGE}"
                    )

            except Exception as ex:
                return (
                    f"Please give your timezone correctly \n {Constants.HELP_MESSAGE}"
                )

        elif first_word == "broadcast" or first_word == "/broadcast":
            if chat_id == Constants.BROADCAST_CHAT_ID:
                normalized_text = " ".join(split_text[1:])
                if str.isspace(normalized_text) or normalized_text == "":
                    return f"There is no sentence found after the word *broadcast*."
                else:
                    await Events.broadcast_message(normalized_text)
                    return "Broadcast is sent"
            else:
                return "You have no broadcast right"
        elif first_word == "status" or first_word == "/status":
            gmt, active = get_user_status(chat_id)
            if gmt is None:
                return "You have not joined the system yet, please type, *join*."
            else:
                return (
                    f"Your current status:"
                    f"\n- Gmt: *GMT{gmt}*"
                    f"\n- Daily sending is active: *{active}*"
                )
        elif first_word == "feedback" or first_word == "/feedback":

            message = " ".join(split_text[1:])
            message_with_user_information = message + f"\nFrom the user: *{name}* \nchat id: *{chat_id}*"

            if str.isspace(message) or message == "":
                return f"There is no message found after the word *feedback*."
            else:
                success = await Events.send_a_message_to_user(Constants.FEEDBACK_FORWARD_CHAT_ID, message_with_user_information)
                if success:
                    return f"I forwarded your feedback to the admin, thank you for your support.\nFeedback: *{message}*"
                else:
                    return f"I could not forward your feedback to the admin, an error occurred."

        elif first_word == "support" or first_word == "/support":
            return (
                f"Thank you, to support me you can"
                f"\n- Share me with your friends"
                f"\n- Give feedback using the command, *feedback sentence*"
                f"\n- Star the github repository at https://github.com/FarukOzderim/Memory-Vault/"
            )

        else:
            return f"{name}, I do not know that command.{Constants.HELP_MESSAGE}"
