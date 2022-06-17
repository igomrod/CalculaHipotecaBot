import logging
from telegram.constants import ParseMode
from apps.telegram_bot import serializers
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from core.application.dtos import LoanDTO
from core.application.services import get_loans
from core.infrastructure import loan_repository


logger = logging.getLogger(__name__)

# conversation states
CHOOSING = 0


def display_name(loan: LoanDTO):
    return f'{loan.loan_summary.amount} al {loan.loan_summary.tae}% durante {loan.loan_summary.term} años'


async def entrypoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    context.user_data['loans'] = get_loans(owner_id=str(update.effective_chat.id), repository=loan_repository)

    if len(context.user_data['loans']) == 0:
        await update.message.reply_text(
            "Crea una nueva hipoteca con /crearNuevaHipoteca",
        )
        return ConversationHandler.END

    reply_keyboard = [
        [display_name(loan) for loan in context.user_data['loans']],
    ]

    await update.message.reply_text(
        "Selecciona la hipoteca para ver la tabla de amortización y el resumen",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CHOOSING


async def mortgage_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    def find_loan_by_display_name(display_name_search, loans):
        return [loan for loan in loans if display_name(loan) in display_name_search][0]

    loan_display_name = update.message.text
    await update.message.reply_text(f"Vale! Estoy generando la info para la hipoteca:  {loan_display_name}?")

    owner_loans = context.user_data['loans']

    selected_loan = find_loan_by_display_name(loan_display_name, owner_loans)

    if not selected_loan:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"No encuentro esa hipoteca, selecciona una valida")

        return CHOOSING

    await send_mortgage_info(context, update, selected_loan)

    return ConversationHandler.END


async def send_mortgage_info(context, update, loan):
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(f'/tmp/{update.effective_chat.id}_{loan.loan_id}.png', 'rb'))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{(serializers.loan_summary_to_table_string(loan.summary()))}", parse_mode=ParseMode.MARKDOWN_V2)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("misHipotecas", entrypoint)],
    states={
        CHOOSING: [
            MessageHandler(
                filters.TEXT,
                mortgage_selected
            )
        ]
    },
    fallbacks=[MessageHandler(filters.TEXT, mortgage_selected)]
)
