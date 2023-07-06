from asgiref.sync import sync_to_async
from telegram import constants as telegram_constants
from users.models import User


async def get_user(update):
    uid = update.effective_user.id
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=uid)
        return user
    except BaseException:
        return False


async def check_subscription(update, context):
    member = await context.bot.get_chat_member(chat_id='@fizika_na_izi', user_id=update.effective_user.id)
    if member:
        match member.status:
            case telegram_constants.ChatMemberStatus.ADMINISTRATOR:
                return True
            case telegram_constants.ChatMemberStatus.MEMBER:
                return True
            case telegram_constants.ChatMemberStatus.OWNER:
                return True
    return False
