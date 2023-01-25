import random
import os
import sys

from typing import List
import datetime
import asyncio
from httpx import AsyncClient, Response

from .message_validations import ResponseToMessage
from .db import db_read_users, Reminder, User
from .constants import Constants
from .packages import Packages


class Events:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    TELEGRAM_SET_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    TELEGRAM_COPY_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/copyMessage"

    PORT = 8000
    HOST_URL = None
    SELF_SIGNED = False

    @classmethod
    async def main_event(cls) -> None:
        """
        Main Event Loop

        Runs in a while loop, Triggers Events.send_user_hourly_memories at every hour.
        """
        while True:
            await asyncio.sleep(cls.get_time_until_next_hour())
            async with AsyncClient() as client:
                endpoint = f"http://0.0.0.0:{cls.PORT}/trigger_send_user_hourly_memories/{Events.TOKEN}"
                response = await client.post(url=endpoint)

    @classmethod
    def get_time_until_next_hour(cls) -> float:
        # Ref: https://stackoverflow.com/a/52808375/15282482
        delta = datetime.timedelta(hours=1)
        now = datetime.datetime.now()
        next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
        return (next_hour - now).total_seconds()

    @classmethod
    def send_user_hourly_memories(
        cls,
        user: User,
        hour: int,
    ) -> None:
        """
        Sends memories to user if the current_hour is in his schedule.
        """
        hour = (hour + user.gmt) % 24
        if user.scheduled_hours == "":
            return
        scheduled_hours = user.scheduled_hours.split(",")
        number_of_messages_at_this_hour = 0

        for str_hour in scheduled_hours:
            if (
                int(str_hour) > hour
            ):  # Scheduled_hours are sorted, next items will be > hour as well.
                break
            if int(str_hour) == hour:
                number_of_messages_at_this_hour += 1
        number_of_messages_at_this_hour = min(
            len(user.reminders), number_of_messages_at_this_hour
        )
        selected_reminders = random.sample(
            user.reminders, number_of_messages_at_this_hour
        )
        for reminder in selected_reminders:  # Send the memory in background
            asyncio.create_task(
                cls.send_a_message_to_user(user.telegram_chat_id, reminder.reminder)
            )
            now = datetime.datetime.now()

    @classmethod
    async def send_message_list_at_background(
        cls,
        telegram_chat_id: int,
        message_list: List[str],
        notify: bool = True,
    ) -> bool:
        for message in message_list:
            await Events.send_a_message_to_user(
                chat_id=telegram_chat_id,
                message=message,
                notify=notify,
            )
        return True

    @classmethod
    async def create_response_message(
        cls,
        message: str,
        chat_id: int,
        convert: bool,
        notify: bool = True,
    ) -> (str, ResponseToMessage):
        """
        Creates the response message

        Runs the related package and sends the resulting message if the reminder is a package type.
        Sends the photo if the message is photo type.
        Sends the document if the message is document type.
        Sends the text if the message is text type.

        Args:
            message:
            chat_id:
            convert: Converts the encoded message to related type of message, if True
            notify: If false, send the message without notifying.

        Returns:
            converted_message:

        """
        message_id = None
        from_chat_id = None
        text = None

        if convert:
            words = message.split(" ")
            if len(words) == 2:
                if words[0] == "package:":
                    fn_id = int(words[1])
                    text = await (Packages.functions[fn_id]())

                elif words[0] == "message_id:":
                    message_id = int(words[1])
                    from_chat_id = chat_id

                else:
                    text = message

        return cls.TELEGRAM_SEND_MESSAGE_URL, ResponseToMessage(
            **{
                "text": text,
                "message_id": message_id,
                "chat_id": chat_id,
                "from_chat_id": from_chat_id,
                "disable_notification": notify,
            }
        )

    @classmethod
    async def send_a_message_to_user(
        cls,
        chat_id: int,
        message: str,
        retry_count: int = 3,
        sleep_time: float = 0.01,
        convert: bool = True,
        notify: bool = True,
    ) -> bool:
        url, message = await cls.create_response_message(message, chat_id, convert)
        print(f"%% {datetime.datetime.now()}: Message is: {message}")

        await asyncio.sleep(sleep_time)
        for retry in range(retry_count):
            # Avoid too many requests error from Telegram
            response = await cls.request(url, message.dict())
            if response.status_code == 200:
                # print(f"%% {datetime.datetime.now()}: Sent message ")
                return True
            elif response.status_code == 429:
                retry_after = int(response.json()["parameters"]["retry_after"])
                print(
                    f"%% {datetime.datetime.now()} Retry After: {retry_after}, message: {message}"
                )
                await asyncio.sleep(retry_after)
            else:
                print(
                    f"%% {datetime.datetime.now()} Unhandled response code: {response.status_code}, response: {response.json()}, chat: {chat_id}, message: {message}, url: {url}"
                )
        return False

    @classmethod
    async def broadcast_message(cls, message: str) -> None:
        users = db_read_users(limit=100000, only_active_users=False)
        await asyncio.gather(
            *(
                Events.send_a_message_to_user(user.telegram_chat_id, message)
                for user in users
            )
        )

    @classmethod
    async def request(cls, url: str, payload: dict, debug: bool = False) -> Response:
        async with AsyncClient(timeout=30 * 60) as client:
            request = await client.post(url, json=payload)
            if debug:
                print(request.json())
            return request

    @classmethod
    async def set_telegram_webhook_url(cls) -> bool:
        if cls.SELF_SIGNED:
            payload = {
                "url": f"{cls.HOST_URL}/webhook/{cls.TOKEN}",
                "certificate": open(os.environ.get("PEM_FILE"), "rb"),
            }
        else:
            payload = {"url": f"{cls.HOST_URL}/webhook/{cls.TOKEN}"}
        req = await cls.request(cls.TELEGRAM_SET_WEBHOOK_URL, payload)
        return req.status_code == 200

    @classmethod
    async def get_public_ip(cls):
        # Reference: https://pytutorial.com/python-get-public-ip

        endpoint = "https://ipinfo.io/json"
        async with AsyncClient() as client:
            response = await client.get(endpoint)

        if response.status_code != 200:
            sys.exit("Could not get the public ip, exiting!")
        data = response.json()

        return data["ip"]
