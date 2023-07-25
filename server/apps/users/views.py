from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404

from .models import User
from .serializers import UserSerializer

# Create your views here.


class GetUserByTelegramId(APIView):
    """
    Получение пользователя по его идентефикатору в Telegram

    Доступно только для бота
    """
    permission_classes = [permissions.AllowAny]

    def get_object(self, telegram_id):
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, telegram_id, format=None):
        user = self.get_object(telegram_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
