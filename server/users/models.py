from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=30, unique=True, verbose_name="Телефон")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    is_active = models.BooleanField(default=True, verbose_name="Профиль активен?")
    is_staff = models.BooleanField(default=False, verbose_name="Права администратора")

    telegram_id = models.CharField(max_length=15, blank=True, unique=True, verbose_name="Id в телеграм")
    telegram_username = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Username в Telegram")

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name
