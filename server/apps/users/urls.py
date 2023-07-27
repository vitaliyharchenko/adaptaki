from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('telegram/',
         views.GetUserByTelegramId.as_view()),
    path('telegram/reg', views.RegTelegramView.as_view())
]
