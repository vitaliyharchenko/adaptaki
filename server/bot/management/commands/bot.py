import logging
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from users.models import User
from .features.auth import get_user, check_subscription
from .features.reg import reg_handler

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, constants as telegram_constants
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


# обработчик команды старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update=update)
    if user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"С возвращением, {user.first_name}!")
    else:
        keyboard = [[InlineKeyboardButton(
            "Зарегистрироваться", callback_data="reg")]]
        markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот с задачами ЕГЭ. Давай знакомиться!", reply_markup=markup)


# обработчик другизх команд, возвращает эхо
async def check_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_subscribed = await check_subscription(update, context)

    if is_subscribed:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'У тебя есть подписка на канал @fizika_na_izi')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Подписка на канал @fizika_na_izi отсутствует')


# обработчик другизх команд, возвращает эхо
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# обработчик коллбеков
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


# объявление переменной бота
application = ApplicationBuilder().token(
    '6097853298:AAFd-KCP9WeVeQBBEQjK8Eknv7cagY27ao4').build()

start_handler = CommandHandler('start', start)
application.add_handler(start_handler)

member_handler = MessageHandler(
    filters.Regex('^member$'), check_member)
application.add_handler(member_handler)

application.add_handler(CallbackQueryHandler(button))

# Процесс регистрации по команде /reg
application.add_handler(reg_handler)

# Название класса обязательно - "Command"


class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        application.run_polling()
