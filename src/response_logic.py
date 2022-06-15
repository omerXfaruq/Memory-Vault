import random
import asyncio

from .db import *
from .events import Events
from .constants import Constants


class ResponseLogic:
    @staticmethod
    async def create_response(
        text: str, name: str, chat_id: int, language_code: str
    ) -> str:

        split_text = text.split(" ")
        first_word = split_text[0]
        user = UserCreate(
            name=name,
            telegram_chat_id=chat_id,
        )

        if ResponseLogic.check_command_type(first_word, "start"):
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
            if len(split_text) == 1:  # send
                memory = select_random_memory(user)
                if memory is None:
                    return Constants.Common.inactive_user(name, language_code)
                elif memory is False:
                    return Constants.Common.no_memory_found(name, language_code)
                else:
                    return memory.reminder
            else:  # send number
                try:
                    number_of_sending = int(split_text[1])
                    if not (1 <= number_of_sending < 50):
                        return Constants.Send.send_count_out_of_bound(
                            name, language_code
                        )
                except:
                    return Constants.Send.send_count_out_of_bound(name, language_code)

                all_memories = list_memories(user)
                if len(all_memories) == 0:
                    return Constants.Common.no_memory_found(name, language_code)

                send_count = min(len(all_memories), number_of_sending)
                selected_memories = random.sample(all_memories, send_count)
                for memory in selected_memories:  # Send the memories in background
                    asyncio.create_task(
                        Events.send_a_message_to_user(
                            user.telegram_chat_id, memory.reminder
                        )
                    )
                return ""

        elif ResponseLogic.check_command_type(first_word, "list"):
            memories = list_memories(user)
            memory_count = len(memories)
            if memories is None:
                return Constants.Common.inactive_user(name, language_code)
            elif memory_count == 0:
                return Constants.Common.no_memory_found(name, language_code)
            else:
                background_message_list = []
                for reminder in memories:
                    background_message_list.append(
                        f"\n{reminder.id}: {reminder.reminder}"
                    )
                asyncio.create_task(
                    Events.send_message_list_at_background(
                        telegram_chat_id=chat_id, message_list=background_message_list
                    )
                )

                response_message = Constants.List.list_messages(name, memory_count, language_code)
                return response_message

        elif ResponseLogic.check_command_type(first_word, "add"):
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

        elif ResponseLogic.check_command_type(first_word, "delete"):
            if len(split_text) < 2:
                return Constants.Delete.no_id(name, language_code)
            else:
                try:
                    memory_id = int(split_text[1])
                    if memory_id < 0:
                        return Constants.Delete.no_id(name, language_code)
                    else:
                        response = delete_memory(user, memory_id)
                        if response is None:
                            return Constants.Common.inactive_user(name, language_code)
                        elif response is False:
                            return Constants.Delete.no_id(name, language_code)
                        else:
                            memory = response

                            return Constants.Delete.success(name, language_code, memory)

                except Exception as ex:
                    return Constants.Delete.no_id(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "schedule"):
            if len(split_text) == 1:
                schedule = get_schedule(user)
                if schedule is None:
                    return Constants.Common.inactive_user(name, language_code)
                elif schedule == "":
                    return Constants.Schedule.empty_schedule(name, language_code)
                else:
                    return Constants.Schedule.success(name, language_code, schedule)

            elif len(split_text) > 1:
                if split_text[1] == "reset":
                    new_schedule = reset_schedule(user)
                    if new_schedule is None:
                        return Constants.Common.inactive_user(name, language_code)
                    else:
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
                count_of_notes = list_memories(user)
                return Constants.Status.get_status(
                    name, language_code, gmt, active, schedule, count_of_notes
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

        elif ResponseLogic.check_command_type(first_word, "deletelast"):
            response = delete_last_memory(user)
            if response is None:
                return Constants.Common.inactive_user(name, language_code)
            elif response is False:
                return Constants.Common.no_memory_found(name, language_code)
            else:
                return Constants.Delete.success(name, language_code, response)

        elif ResponseLogic.check_command_type(first_word, "support"):
            return Constants.Support.support(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial1"):
            return Constants.Tutorial.tutorial_1(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial2"):
            return Constants.Tutorial.tutorial_2(name, language_code)

        elif ResponseLogic.check_command_type(first_word, "tutorial3"):
            return Constants.Tutorial.tutorial_3(name, language_code)

        else:
            return Constants.Common.unknown_command(name, language_code)

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
            or input_command == f"/{correct_command}@memoryvaultbot"
        ):
            return True
        else:
            return False
