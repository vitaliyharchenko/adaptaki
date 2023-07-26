from django.core.management.base import AppCommand
from apps.users.models import User
from rest_framework.authtoken.models import Token


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Create tokens for all users'

    def handle(self, *args, **kwargs):

        users = User.objects.all()

        for u in users:
            token = Token.objects.create(user=u)

        print(f"Tokens created")
