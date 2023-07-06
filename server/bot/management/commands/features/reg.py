from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError
import phonenumbers

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Теперь введите телефон в формате 7XXXXXXXXXX")
    return PHONE


async def phone(update, context):
    phone = "+" + update.message.text

    try:
        phone_number = phonenumbers.parse(phone)
        is_possible_number = phonenumbers.is_possible_number(phone_number)

        if not is_possible_number:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Введен некорректный номер телефона, попробуй снова в формате 7XXXXXXXXXX")
            return PHONE
    except phonenumbers.phonenumberutil.NumberParseException:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Введен некорректный номер телефона, попробуй снова в формате 7XXXXXXXXXX")
        return PHONE
        
    first_name = context.user_data.get('first_name', 'Not found')
    last_name = context.user_data.get('last_name', 'Not found')

    try:
        user = await sync_to_async(User.objects.create_user)(phone=phone)
    except IntegrityError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Пользователь с таким номером телефона уже существует в базе. Обратитесь к админу @vitaliyharchenko для ее устранения")
        print("Неуникальный телефон", e)
        return ConversationHandler.END
    except BaseException:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"При регистрации произошла ошибка. Обратитесь к админу @vitaliyharchenko для ее устранения")
        print("Не получилось зарегистрироваться")
        return ConversationHandler.END

    user = await sync_to_async(User.objects.get)(phone=phone)
    user.first_name = first_name
    user.last_name = last_name
    user.telegram_id = update.effective_user.id
    user.telegram_username = update.effective_user.username
    
    try:
        await sync_to_async(user.save)()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{first_name}, вы успешно зарегистрированы!")
        return ConversationHandler.END
    except BaseException as e:
        print("Телеграм уже был в базе", e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{first_name}, ваш профиль Telegram уже был зарегистрирован")
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
