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


class GetTokenByTelegramId(APIView):
    """
    Получение токена пользователя по его идентефикатору в Telegram

    Доступно только для бота
    """
    permission_classes = [permissions.AllowAny]

    def get_object(self, telegram_id):
        try:
            user = User.objects.get(telegram_id=telegram_id)
            return Token.objects.get(user=user)
        except User.DoesNotExist:
            raise Http404
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            return token.key

    def post(self, request, format=None):
        telegram_id = request.data["telegram_id"]

        key = ''

        try:
            user = User.objects.get(telegram_id=telegram_id)
            token = Token.objects.get(user=user)
            key = token.key
        except User.DoesNotExist:
            return Response({'error': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
            key = token.key

        return Response({'token': key}, status=status.HTTP_200_OK)