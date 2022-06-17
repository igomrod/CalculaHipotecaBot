import pytest

from apps.telegram_bot.app import create_app
from tests.apps.telegram_bot.test_client import TelegramTestClient


@pytest.mark.asyncio
async def test_create_mortgage_flow():
    test_client = TelegramTestClient(create_app())
    await test_client.initialize()

    await test_client.type("/crearNuevaHipoteca")

    await test_client.assert_bot_reply_with(
        'Hola! Te voy a mostrar una tabla de amortiación de hipoteca. Dame los datos?')
