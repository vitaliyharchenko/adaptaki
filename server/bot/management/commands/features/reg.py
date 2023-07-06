from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from .auth import get_user
from users.models import User

# States for conversation
FIRST_NAME = 'REG_FIRST_NAME'
LAST_NAME = 'REG_LAST_NAME'
PHONE = 'REG_PHONE'
CONFIRM = 'CONFIRM'


async def reg_start(update, context):
    user = await get_user(update)

    if user:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{user.first_name} {user.last_name}, вы уже зарегистрированы")
        return ConversationHandler.END
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Для работы в нашем боте нужно пройти короткую регистрацию. Напиши свое имя")
        return FIRST_NAME


async def first_name(update, context):
    first_name = update.message.text
    context.user_data['first_name'] = first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Теперь фамилию")
    return LAST_NAME


async def last_name(update, context):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Теперь телефон")
    return PHONE


async def phone(update, context):
    phone = update.message.text
    context.user_data['user_phone'] = phone

    first_name = context.user_data.get('first_name', 'Not found')
    last_name = context.user_data.get('last_name', 'Not found')

    print(first_name)
    print(last_name)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Спасибо, {first_name} {last_name}! Пробуем создать профиль, привязанный к телефону: {phone}")

    try:
        user = await sync_to_async(User.objects.create_user)(phone=phone)
        print("Create user", user)
        user.first_name = first_name
        user.last_name = last_name
        user.telegram_id = update.effective_user.id
        user.telegram_username = update.effective_user.username
        user.save()

    except IntegrityError:
        print("Пользователь с такими данными уже существует")
    except BaseException:
        print("Не получилось зарегистрироваться")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Чтобы зарегистрироваться снова нажми на команду /reg")

    return ConversationHandler.END


# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
reg_handler = ConversationHandler(
    entry_points=[CommandHandler("reg", reg_start)],
    states={
        PHONE: [MessageHandler(filters.TEXT, phone)],
        FIRST_NAME: [MessageHandler(filters.TEXT, first_name)],
        LAST_NAME: [MessageHandler(filters.TEXT, last_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
