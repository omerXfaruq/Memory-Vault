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

    CURRENT_TIMEZONE = int(datetime.datetime.now(datetime.timezone.utc).astimezone().tzname())

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
        timezone: int,
        memory_list: List[Reminder],
    ) -> bool:
        """
        Waits until users midday according to the timezone. Then sends a random reminder from the memory vault.

        Args:
            user_id:
            telegram_id:
            timezone:
            memory_list:

        Returns: True if successful
        """

        length = len(memory_list)
        if length == 0:
            return True
        random_index = random.randint(0, length - 1)
        random_element = memory_list[random_index].reminder

        waiting_duration = 0
        if timezone > 0:
            waiting_duration = datetime.timedelta(hours=24 - timezone).total_seconds()
        elif timezone < 0:
            waiting_duration = datetime.timedelta(hours=-timezone).total_seconds()
        # Wait until reaching midday on that timezone
        await asyncio.sleep(waiting_duration)

        success = await cls.send_a_message_to_user(telegram_id, random_element)
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
    async def request(cls, url: str, payload: dict, debug: bool = False):
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
