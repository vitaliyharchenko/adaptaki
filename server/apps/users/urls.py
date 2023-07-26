from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('check/telegram/<int:telegram_id>/',
         views.GetUserByTelegramId.as_view()),
    path('telegram-token-auth/',
         views.GetTokenByTelegramId.as_view()),
]
