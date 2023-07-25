from django.urls import path
from . import views


urlpatterns = [
    path('check/telegram/<int:telegram_id>/',
         views.GetUserByTelegramId.as_view()),
]
