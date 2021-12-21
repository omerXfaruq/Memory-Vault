import pytest
import asyncio

from src.events import Events

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_send_message():
    response = await Events.single_user_mail(1, 861126057)
    assert response


@pytest.mark.asyncio
async def test_main_event():
    await Events.main_event()


@pytest.mark.asyncio
def test_time_until_midday():
    print(Events.get_time_until_midday())
