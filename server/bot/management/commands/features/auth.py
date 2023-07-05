from asgiref.sync import sync_to_async
from users.models import User


async def get_user(update):
    uid = update.effective_user.id
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=uid)
        return user
    except BaseException:
        return False