from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.UserDetailView.as_view(), name='user-update'),
    path('social-auth-redirect/', views.social_auth_redirect,
         name='social-auth-redirect'),
]
