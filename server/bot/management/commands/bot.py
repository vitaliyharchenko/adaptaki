import logging
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from users.models import User
from .features.auth import get_user, check_subscription
from .features.reg import reg_handler

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, constants as telegram_constants
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# обработчик команды старт
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update=update)
    if user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"С возвращением, {user.first_name}!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот с задачами ЕГЭ. Давай знакомиться! Чтобы воспользоваться мной, нужно пройти простую регистрацию. Для этого нажми /reg")


async def menu_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="m1"),
            InlineKeyboardButton("Option 2", callback_data="m2"),
            InlineKeyboardButton("Option 3", callback_data="m3"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Главное меню", reply_markup=reply_markup)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update=update)

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="m1"),
            InlineKeyboardButton("Option 2", callback_data="m2"),
            InlineKeyboardButton("Option 3", callback_data="m3"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Главное меню", reply_markup=reply_markup)


async def first_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user(update=update)

    query = update.callback_query
    await query.answer()

    keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Первое меню", reply_markup=reply_markup)


# обработчик другизх команд, возвращает эхо
async def check_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_subscribed = await check_subscription(update, context)

    if is_subscribed:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'У тебя есть подписка на канал @fizika_na_izi')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Подписка на канал @fizika_na_izi отсутствует')


# обработчик коллбеков
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    match query.data:
        case 'reg':
            print("reg")
        case _:
            print("unknown query")

    await query.edit_message_text(text=f"Selected option: {query.data}")


# объявление переменной бота
application = ApplicationBuilder().token(
    '6097853298:AAGbBS8rfloSwbcOhqwRP3kaLfGfJH687uA').build()

start_handler = CommandHandler('start', start_handler)
application.add_handler(start_handler)

member_handler = MessageHandler(
    filters.Regex('^member$'), check_member)
application.add_handler(member_handler)


# Процесс регистрации по команде /reg
application.add_handler(reg_handler)

# Обработка меню
application.add_handler(CommandHandler('menu', menu_start))
application.add_handler(CallbackQueryHandler(menu_handler, pattern='main'))
application.add_handler(CallbackQueryHandler(first_menu_handler, pattern='m1'))

# Название класса обязательно - "Command"
class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    def handle(self, *args, **kwargs):
        application.run_polling()
