# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from apps.telegram_bot.user_data import validate_user_data, parse_user_data
from core.application.dtos import CreateLoanCommand
from core.application.services import create_loan
from core.infrastructure import loan_repository
from core.infrastructure.save_as_image import save_as_image

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Años", "Meses", "Capital", "TAE"],
    ["Cuantos meses mostrar? (por defecto 12)", "Amortizaciones Parciales"],
    ["Generar Tabla"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def format_current_data(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Hola! Te voy a mostrar una tabla de amortiación de hipoteca. Dame los datos?",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    if not validate_user_data(user_data):
        await update.message.reply_text(
            f"Necesito, Años o Meses, Capital y TAE para generar la tabla",
            reply_markup=ReplyKeyboardRemove(),
        )

        await update.message.reply_text(
            "Dame más datos?",
            reply_markup=markup,
        )
        return CHOOSING

    try:
        request: CreateLoanCommand = parse_user_data(user_data, update.effective_chat.id)
    except ValueError:
        await update.message.reply_text(
            f"Alguna de tus datos son incorrectos, por favor asegurate de que los numeros estan en formato adeducado",
            reply_markup=markup,
        )
        return CHOOSING

    create_loan(request,
                repository=loan_repository,
                save_as_image_service=save_as_image)

    user_data.clear()
    return ConversationHandler.END


async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Vale! Dime {text.lower()}?")

    return TYPING_REPLY


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Vale! Estos son los datos que me has proporcionado:"
        f"{format_current_data(user_data)}",
        reply_markup=markup,
    )

    return CHOOSING

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("crearNuevaHipoteca", entrypoint)],
    states={
        CHOOSING: [
            MessageHandler(
                filters.Regex("^(Años|Meses|Capital|TAE|Cuantos\ meses\ mostrar\?\ \(por\ defecto\ 12\))$"),
                regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Generar Tabla$")),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Generar Tabla"), done)],
)