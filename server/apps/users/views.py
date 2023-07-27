from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import Http404

from .models import User
from .serializers import UserSerializer

# Create your views here.


class GetUserByTelegramId(APIView):
    """
    Получение пользователя по его идентефикатору в Telegram

    Доступно только для бота

    Для проверки: curl -d "telegram_id=123&secret_code=228" http://127.0.0.1:8000/users/telegram/  
    """
    permission_classes = [permissions.AllowAny]

    def get_object(self, telegram_id):
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        telegram_id = request.data["telegram_id"]
        secret_code = request.data["secret_code"]

        if secret_code != "228":
            return Response({"error": "Bad secret code from telegram bot"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object(telegram_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegTelegramView(APIView):
    """
    Регистрация пользователя Telegram

    Передаем {first_name, last_name, phone, class_of, telegram_id, telegram_username}
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        phone = "+" + request.data["phone"]
        class_of = request.data["class_of"]
        telegram_id = request.data["telegram_id"]
        secret_code = request.data["secret_code"]

        if secret_code != "228":
            return Response({"error": "Bad secret code from telegram bot"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(phone=phone, first_name=first_name,
                                       last_name=last_name, class_of=class_of, telegram_id=telegram_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Cannot register user: {e}"}, status=status.HTTP_400_BAD_REQUEST)
