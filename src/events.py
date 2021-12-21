import random
import os

import datetime
import asyncio
from httpx import AsyncClient

from message_validations import MessageBodyModel, ResponseToMessage


class Events:
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    TELEGRAM_SET_WEBHOOK_URL = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    HOST_URL = None

    CURRENT_TIMEZONE = +3
    receivers = {
        1: [861126057, +3],
        2: [1044137329, +3],
    }

    memory_vaults = {
        1: [
            "Time is money",
            "Follow smart person's focus",
            "When there is a doubt, take an action and destroy it",
        ],
        2: [
            "Time is money",
            "Follow smart person's focus",
            "When there is a doubt, take an action and destroy it",
        ],
    }

    @classmethod
    async def main_event(cls) -> None:
        """
        Main Event Loop

        Runs in a while loop, Triggers Events.single_user_mail for each user every midday.
        """
        while True:
            await asyncio.sleep(cls.get_time_until_midday())

            await asyncio.gather(
                *(
                    Events.single_user_mail(
                        user_id,
                        telegram_id,
                        timezone - cls.CURRENT_TIMEZONE
                    )
                    for user_id, [telegram_id, timezone] in cls.receivers.items()
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
    async def single_user_mail(cls, user_id: int, telegram_id: int, timezone: int) -> bool:
        """
        Waits until users midday according to the timezone. Then sends a random reminder from the memory vault.
        :param user_id:
        :param telegram_id:
        :param timezone:
        :return: True if successful
        """
        waiting_duration = 0
        if timezone > 0:
            waiting_duration = datetime.timedelta(hours=24 - timezone).total_seconds()
        elif timezone < 0:
            waiting_duration = datetime.timedelta(hours=-timezone).total_seconds()
        # Wait until reaching midday on that timezone
        await asyncio.sleep(waiting_duration)

        memory_list = cls.memory_vaults[user_id]
        random_element = random.choice(memory_list)
        if_true = await cls.send_a_message_to_user(telegram_id, random_element)
        return if_true

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
        payload = {
            "url": f"{cls.HOST_URL}/webhook/{cls.TOKEN}"
        }
        req = await cls.request(cls.TELEGRAM_SET_WEBHOOK_URL, payload)
        return req.status_code == 200
