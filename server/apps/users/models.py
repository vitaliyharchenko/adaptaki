from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework.authtoken.models import Token

from .managers import UserManager


CLASSES = (
    ('parent', 'Родитель'),
    ('old', 'Выпускник'),
    ('2024', '11 класс'),
    ('2025', '10 класс'),
    ('2026', '9 класс'),
    ('2027', '8 класс'),
    ('2028', '7 класс'),
)


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        max_length=30, unique=True, verbose_name="Телефон")
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name="Фамилия")
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации")
    is_active = models.BooleanField(
        default=True, verbose_name="Профиль активен?")
    is_staff = models.BooleanField(
        default=False, verbose_name="Права администратора")
    class_of = models.CharField(
        max_length=10, choices=CLASSES, blank=True, verbose_name="Класс")

    telegram_id = models.CharField(
        max_length=15, blank=True, unique=True, null=True, verbose_name="Id в телеграм")
    telegram_username = models.CharField(
        max_length=50, blank=True, unique=True, null=True, verbose_name="Username в Telegram")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def token(self):
        try:
            token = Token.objects.get(user=self)
            return token.key
        except Token.DoesNotExist:
            token = Token.objects.create(user=self)
            return token.key
        except:
            return False
