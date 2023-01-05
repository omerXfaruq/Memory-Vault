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
    TELEGRAM_SEND_DOCUMENT_URL = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

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
        cls, telegram_chat_id: int, message_list: List[str]
    ) -> bool:
        for message in message_list:
            await Events.send_a_message_to_user(
                telegram_id=telegram_chat_id, message=message
            )
        return True

    @classmethod
    async def get_package_message(
        cls,
        message: str,
    ) -> str:
        """
        Runs the related package if the reminder is a package type.

        Args:
            message:

        Returns:
            converted_message

        """
        words = message.split(" ")
        if words[0] == "package:":
            package_id = 0
            try:
                package_id = int(words[1])
            except:
                return message
            return await (Packages.functions[package_id]())

        return message

    @classmethod
    async def send_a_message_to_user(
        cls,
        telegram_id: int,
        message: str,
        retry_count: int = 3,
        sleep_time: float = 0.1,
    ) -> bool:
        message = await cls.get_package_message(message)
        message = ResponseToMessage(
            **{
                "text": message,
                "chat_id": telegram_id,
            }
        )
        await asyncio.sleep(sleep_time)
        for retry in range(retry_count):
            # Avoid too many requests error from Telegram
            response = await cls.request(cls.TELEGRAM_SEND_MESSAGE_URL, message.dict())
            if response.status_code == 200:
                print(f"%% {datetime.datetime.now()}: Sent message {retry}")
                return True
            elif response.status_code == 429:
                retry_after = int(response.json()["parameters"]["retry_after"])
                print(f"%% {datetime.datetime.now()} Retry After: {retry_after}, message: {message}")
                await asyncio.sleep(retry_after)
            else:
                print(
                    f"%% {datetime.datetime.now()} Unhandled response code: {response.status_code}, response: {response.json()}"
                )
        return False

    @classmethod
    async def broadcast_message(cls, message: str) -> None:
        users = db_read_users(limit=100000, only_active_users=False)
        await asyncio.gather(
            *(
                Events.send_a_message_to_user(
                    user.telegram_chat_id,
                    message,
                )
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
    def archive_db(cls) -> bool:
        command = f'curl -v -F "chat_id={Constants.BROADCAST_CHAT_ID}" -F document=@database.db {cls.TELEGRAM_SEND_DOCUMENT_URL}'
        os.system(command)

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
