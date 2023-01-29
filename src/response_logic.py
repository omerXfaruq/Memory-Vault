import datetime
import random
import asyncio

from .db import *
from .events import Events
from .constants import Constants
from .packages import Packages
from .message_validations import Message


class ResponseLogic:
    @staticmethod
    async def create_response(
        message: Message | None,
        name: str,
        chat_id: int,
        language_code: str,
        text: str = "",
    ) -> str:
        text = message.text or text if message else text

        # Edge case check for "add\nSentence"
        line_split_text = text.split("\n")
        line_split_first_word = line_split_text[0]
        split_text = text.split(" ")
        first_word = split_text[0]

        user = UserCreate(
            name=name,
            telegram_chat_id=chat_id,
        )
        if ResponseLogic.check_command_type(
            first_word, "add"
        ) or ResponseLogic.check_command_type(line_split_first_word, "add"):
            if ResponseLogic.check_command_type(line_split_first_word, "add"):
                memory = "\n".join(line_split_text[1:])
            else:
                memory = " ".join(split_text[1:])
            if str.isspace(memory) or memory == "":
                return Constants.Add.no_sentence(name, language_code)
            else:
                reminder = add_memory(user, memory)
                if reminder is None:
                    return Constants.Common.inactive_user(name, language_code)
                elif reminder is False:
                    return Constants.Add.already_added(name, language_code)
                else:
                    memory = reminder.reminder
                    return Constants.Add.success(name, language_code, memory)

        elif ResponseLogic.check_command_type(first_word, "start"):
            user = join_user(user)
            await Events.send_a_message_to_user(chat_id, Constants.hello)
            return Constants.Start.start_message(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "help"):
            message = Constants.Help.help_message(name, language_code)
            return message

        elif ResponseLogic.check_command_type(first_word, "join"):
            user = join_user(user)

            if user is not None:
                return Constants.Join.successful_join(name, language_code)
            else:
                return Constants.Join.already_joined(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "leave"):
            user = leave_user(user)
            if user is not None and user.telegram_chat_id == chat_id:
                return Constants.Leave.successful_leave(name, language_code)
            else:
                return Constants.Leave.already_left(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "send"):
            send_count = 1  # send
            if len(split_text) == 2:
                try:
                    send_count = int(split_text[1])
                    if not (1 <= send_count < 50):
                        return Constants.Send.send_count_out_of_bound(
                            name, language_code
                        )
                except:
                    return Constants.Send.send_count_out_of_bound(name, language_code)

            memories = select_random_memories(user, count=send_count)
            if memories is None:
                return Constants.Common.inactive_user(name, language_code)
            elif not memories:
                return Constants.Common.no_memory_found(name, language_code)
            else:
                asyncio.create_task(
                    Events.send_message_list_at_background(
                        user.telegram_chat_id, [memory.reminder for memory in memories]
                    )
                )
                return ""

        elif ResponseLogic.check_command_type(first_word, "package"):
            if len(split_text) == 1:  # package
                return Constants.Package.help(name, language_code)
            elif len(split_text) >= 3:
                if split_text[1] == "add":
                    package_id = 0
                    try:
                        package_id = int(split_text[2])
                    except:
                        return Constants.Package.incorrect_id(name, language_code)

                    if package_id >= len(Packages.functions) or package_id < 0:
                        return Constants.Package.incorrect_id(name, language_code)

                    success = add_package(user, package_id)
                    if not success:
                        return Constants.Package.already_added(name, language_code)

                    return Constants.Package.success(name, language_code, package_id)
            else:
                return Constants.Package.incorrect_id(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "list"):
            memories = list_memories(user)

            if memories is None:
                return Constants.Common.inactive_user(name, language_code)
            memory_count = len(memories)
            if memory_count == 0:
                return Constants.Common.no_memory_found(name, language_code)
            else:
                background_message_list = []
                for message_id, reminder in enumerate(memories):
                    background_message_list.append(f"*{message_id}*: ")
                    background_message_list.append(reminder.reminder)

                asyncio.create_task(
                    Events.send_message_list_at_background(
                        telegram_chat_id=chat_id,
                        message_list=background_message_list,
                        notify=False,
                    )
                )

                response_message = Constants.List.list_messages(
                    name, memory_count, language_code
                )
                return response_message

        elif ResponseLogic.check_command_type(first_word, "del"):
            resp = delete_last_sent_memory(user)
            if resp is None:
                return Constants.Common.inactive_user(name, language_code)
            elif resp is False:
                return Constants.Delete.no_message(name, language_code)
            else:
                memory = resp
                await Events.send_a_message_to_user(
                    chat_id, Constants.Delete.success(name, language_code)
                )
                await Events.send_a_message_to_user(chat_id, memory)
                return ""

        elif ResponseLogic.check_command_type(first_word, "schedule"):
            if len(split_text) == 1:
                schedule = get_schedule(user)
                if schedule is None:
                    return Constants.Common.inactive_user(name, language_code)
                elif schedule == "":
                    return Constants.Schedule.empty_schedule(name, language_code)
                else:
                    schedule = ResponseLogic.readable_schedule(schedule)
                    return Constants.Schedule.success(name, language_code, schedule)

            elif len(split_text) > 1:
                if split_text[1] == "reset":
                    new_schedule = reset_schedule(user)
                    if new_schedule is None:
                        return Constants.Common.inactive_user(name, language_code)
                    else:
                        new_schedule = ResponseLogic.readable_schedule(new_schedule)
                        return Constants.Schedule.success(
                            name, language_code, new_schedule
                        )

                elif split_text[1] == "add":
                    str_numbers = []
                    preceding_text = " ".join(split_text[2:])
                    if str.isspace(preceding_text) or preceding_text == "":
                        return Constants.Schedule.no_number_found(name, language_code)

                    number_check = True
                    try:
                        for str_number in split_text[2:]:
                            number = int(str_number)
                            str_numbers.append(number)
                            if not (0 <= number <= 23):
                                number_check = False
                                break
                    except:
                        return Constants.Schedule.add_incorrect_number_input(
                            name, language_code
                        )

                    if not number_check:
                        return Constants.Schedule.add_incorrect_number_input(
                            name, language_code
                        )

                    else:
                        new_schedule = add_hours_to_the_schedule(user, str_numbers)
                        if new_schedule is None:
                            return Constants.Common.inactive_user(name, language_code)
                        else:
                            new_schedule = ResponseLogic.readable_schedule(new_schedule)
                            return Constants.Schedule.success(
                                name, language_code, new_schedule
                            )

                elif split_text[1] == "remove":
                    preceding_text = " ".join(split_text[2:])
                    number_check = True
                    if str.isspace(preceding_text) or preceding_text == "":
                        return Constants.Schedule.remove_incorrect_number_input(
                            name, language_code
                        )
                    else:
                        try:
                            str_number = split_text[2]
                            number = int(str_number)
                            if not (0 <= number <= 23):
                                number_check = False
                        except:
                            return Constants.Schedule.remove_incorrect_number_input(
                                name, language_code
                            )

                        if not number_check:
                            return Constants.Schedule.remove_incorrect_number_input(
                                name, language_code
                            )

                        else:
                            new_schedule = remove_hour_from_schedule(
                                user, int(str_number)
                            )
                            if new_schedule is None:
                                return Constants.Common.inactive_user(
                                    name, language_code
                                )
                            else:
                                new_schedule = ResponseLogic.readable_schedule(
                                    new_schedule
                                )
                                return Constants.Schedule.success(
                                    name, language_code, new_schedule
                                )

                else:
                    return Constants.Schedule.unknown_command(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "gmt"):
            try:
                gmt = int(split_text[1])
            except Exception as ex:
                return Constants.Gmt.incorrect_timezone(name, language_code)
            if not (-12 <= gmt <= 12):
                return Constants.Gmt.incorrect_timezone(name, language_code)
            else:
                user = update_gmt(user, gmt)
                if user is None:
                    return Constants.Common.inactive_user(name, language_code)
                else:
                    return Constants.Gmt.success(name, language_code, user.gmt)

        elif ResponseLogic.check_command_type(first_word, "broadcast"):
            if not chat_id == Constants.BROADCAST_CHAT_ID:
                return Constants.Broadcast.no_right(name, language_code)
            else:
                normalized_text = " ".join(split_text[1:])
                if str.isspace(normalized_text) or normalized_text == "":
                    return Constants.Broadcast.no_sentence_found(name, language_code)
                else:
                    await Events.broadcast_message(normalized_text)
                    return Constants.Broadcast.success(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "status"):
            gmt, active = get_user_status(chat_id)
            if gmt is None:
                return Constants.Common.inactive_user(name, language_code)
            else:
                schedule = get_schedule(user)
                schedule = ResponseLogic.readable_schedule(schedule)
                memory_count = len(list_memories(user))
                return Constants.Status.get_status(
                    name, language_code, gmt, active, schedule, memory_count
                )

        elif ResponseLogic.check_command_type(first_word, "feedback"):

            message = " ".join(split_text[1:])
            message_with_user_information = (
                message + f"\nFrom the user: *{name}* \nchat id: *{chat_id}*"
            )

            if str.isspace(message) or message == "":
                return Constants.Feedback.no_message(name, language_code)
            else:
                success = await Events.send_a_message_to_user(
                    Constants.FEEDBACK_FORWARD_CHAT_ID, message_with_user_information
                )
                if success:
                    return Constants.Feedback.success(name, language_code, message)
                else:
                    return Constants.Feedback.fail(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "undo"):
            memory = delete_last_memory(user)
            if memory is None:
                return Constants.Common.inactive_user(name, language_code)
            elif memory is False:
                return Constants.Common.no_memory_found(name, language_code)
            else:
                await Events.send_a_message_to_user(
                    chat_id, Constants.Delete.success(name, language_code)
                )
                await Events.send_a_message_to_user(chat_id, memory)
                return ""

        elif ResponseLogic.check_command_type(first_word, "support"):
            return Constants.Support.support(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial1"):
            return Constants.Tutorial.tutorial_1(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial2"):
            return Constants.Tutorial.tutorial_2(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial3"):
            return Constants.Tutorial.tutorial_3(name, language_code)

        else:
            reminder = add_memory(
                user,
                f"message_id: {message.message_id}",
            )
            if reminder is None:
                return Constants.Common.inactive_user(name, language_code)
            elif reminder is False:
                return Constants.Add.already_added(name, language_code)
            else:
                memory = reminder.reminder
                await Events.send_a_message_to_user(chat_id, memory)
                return Constants.Add.success(name, language_code, memory)

    @staticmethod
    def readable_schedule(schedule: str) -> str:
        readable_schedule = ""
        schedule_list = schedule.split(",")
        hour_counts = [0] * 24
        for hour in schedule_list:
            hour = int(hour)
            hour_counts[hour] += 1
        for hour, count in enumerate(hour_counts):
            if count != 0:
                readable_schedule += f"{hour}:00 - {hour_counts[hour]}\n"
        return readable_schedule

    @staticmethod
    def check_command_type(input_command: str, correct_command: str) -> bool:
        """
        Checks the first word of the command, which starts the decision tree.

        Args:
            input_command:
            correct_command:

        Returns: bool

        """
        input_command = input_command.lower()
        if (
            input_command == correct_command
            or input_command == f"/{correct_command}"
            or input_command == f"/{correct_command}@memory_vault_bot"
        ):
            return True
        else:
            return False
