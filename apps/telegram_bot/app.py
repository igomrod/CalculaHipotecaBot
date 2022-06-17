import logging
import os

from dotenv import load_dotenv
from telegram import __version__ as TG_VER

from apps.telegram_bot.commands import create_new_mortgage, list_mortgages

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

load_dotenv()

TOKEN = os.environ['TOKEN']

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


async def direct_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = update.message.text.split(" ")

    user_data = context.user_data

    user_data["Meses"] = args[1]
    user_data["Capital"] = args[2]
    user_data["TAE"] = args[3]
    user_data["Cuantos meses mostrar? (por defecto 12)"] = args[4]
    user_data["Amortizaciones Parciales"] = args[5].replace("-", " - ")

    await create_new_mortgage.done(update, context)


def create_app() -> Application:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(create_new_mortgage.conv_handler)
    application.add_handler(list_mortgages.conv_handler)
    application.add_handler(CommandHandler("tabla", direct_table)) ## TODO Remove

    return application


def bot_start() -> None:
    """Run the bot."""
    application = create_app()

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
