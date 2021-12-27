import random
import os
import sys

from typing import List
import datetime
import asyncio
from httpx import AsyncClient

from .message_validations import ResponseToMessage
from .db import db_read_users, Reminder


class Events:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    TELEGRAM_SET_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    HOST_URL = None

    CURRENT_TIMEZONE = 0

    @classmethod
    async def main_event(cls) -> None:
        """
        Main Event Loop

        Runs in a while loop, Triggers Events.single_user_mail for each user every midday.
        """
        while True:
            await asyncio.sleep(cls.get_time_until_midday())
            users = db_read_users(limit=100000)
            await asyncio.gather(
                *(
                    Events.single_user_mail(
                        user.id,
                        user.telegram_chat_id,
                        user.gmt - cls.CURRENT_TIMEZONE,
                        user.reminders,
                    )
                    for user in users
                )
            )

    @classmethod
    def get_time_until_midday(cls, hour: int = 12, minute: int = 0) -> float:
        now = datetime.datetime.now()
        midday = datetime.datetime(now.year, now.month, now.day, hour, minute)
        if midday >= now:
            waiting_duration = midday - now
        else:
            waiting_duration = midday - now + datetime.timedelta(hours=24)

        return waiting_duration.total_seconds()

    @classmethod
    async def single_user_mail(
        cls,
        user_id: int,
        telegram_id: int,
        timezone_difference: int,
        memory_list: List[Reminder],
    ) -> bool:
        """
        Waits until users midday according to the timezone. Then sends a random reminder from the memory vault.

        Args:
            user_id:
            telegram_id:
            timezone_difference:
            memory_list:

        Returns: True if successful
        """

        length = len(memory_list)
        if length == 0:
            return True
        random_index = random.randint(0, length - 1)
        random_memory = memory_list[random_index].reminder

        waiting_duration = 0
        if timezone_difference > 0:
            waiting_duration = datetime.timedelta(hours=24 - timezone_difference).total_seconds()
        elif timezone_difference < 0:
            waiting_duration = datetime.timedelta(hours=-timezone_difference).total_seconds()
        # Wait until reaching midday on that timezone
        await asyncio.sleep(waiting_duration)

        success = await cls.send_a_message_to_user(telegram_id, random_memory)
        return success

    @classmethod
    async def send_a_message_to_user(cls, telegram_id: int, message: str) -> bool:
        message = ResponseToMessage(
            **{
                "text": message,
                "chat_id": telegram_id,
            }
        )
        req = await cls.request(cls.TELEGRAM_SEND_MESSAGE_URL, message.dict())
        return req.status_code == 200

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
    async def request(cls, url: str, payload: dict, debug: bool = True):
        async with AsyncClient() as client:
            request = await client.post(url, json=payload)
            if debug:
                print(request.json())
            return request

    @classmethod
    async def set_telegram_webhook_url(cls) -> bool:
        payload = {"url": f"{cls.HOST_URL}/webhook/{cls.TOKEN}"}
        req = await cls.request(cls.TELEGRAM_SET_WEBHOOK_URL, payload)
        return req.status_code == 200

    @classmethod
    async def get_public_ip(cls):
        # Reference: https://pytutorial.com/python-get-public-ip

        endpoint = 'https://ipinfo.io/json'
        async with AsyncClient() as client:
            response = await client.get(endpoint)

        if response.status_code != 200:
            sys.exit("Could not get the public ip, exiting!")
        data = response.json()

        return data['ip']
