"""
Фикстуры для тестов приложения users
"""

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_test_user(email='test@example.com', password='testpass123', **kwargs):
    """
    Создает тестового пользователя

    Args:
        email (str): Email пользователя
        password (str): Пароль пользователя
        **kwargs: Дополнительные поля пользователя

    Returns:
        User: Созданный пользователь
    """
    defaults = {
        'first_name': 'Test',
        'last_name': 'User',
        'is_active': True,
    }
    defaults.update(kwargs)

    return User.objects.create_user(
        email=email,
        password=password,
        **defaults
    )


def create_test_superuser(email='admin@example.com', password='adminpass123', **kwargs):
    """
    Создает тестового суперпользователя

    Args:
        email (str): Email суперпользователя
        password (str): Пароль суперпользователя
        **kwargs: Дополнительные поля пользователя

    Returns:
        User: Созданный суперпользователь
    """
    defaults = {
        'first_name': 'Admin',
        'last_name': 'User',
    }
    defaults.update(kwargs)

    return User.objects.create_superuser(
        email=email,
        password=password,
        **defaults
    )


def get_authenticated_client(user):
    """
    Создает аутентифицированный API клиент

    Args:
        user (User): Пользователь для аутентификации

    Returns:
        APIClient: Аутентифицированный клиент
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client


def get_token_authenticated_client(user):
    """
    Создает API клиент с JWT токеном

    Args:
        user (User): Пользователь для получения токена

    Returns:
        tuple: (APIClient, access_token)
    """
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client, access_token


def get_valid_user_data():
    """
    Возвращает валидные данные для создания пользователя

    Returns:
        dict: Валидные данные пользователя
    """
    return {
        'email': 'newuser@example.com',
        'password': 'newpass123',
        'password_confirm': 'newpass123',
        'first_name': 'New',
        'last_name': 'User'
    }


def get_invalid_user_data():
    """
    Возвращает невалидные данные для создания пользователя

    Returns:
        dict: Невалидные данные пользователя
    """
    return {
        'email': 'invalid-email',
        'password': '123',
        'password_confirm': 'different',
        'first_name': '',
        'last_name': ''
    }


def get_update_user_data():
    """
    Возвращает данные для обновления пользователя

    Returns:
        dict: Данные для обновления
    """
    return {
        'first_name': 'Updated',
        'last_name': 'Name'
    }


def get_token_data(user):
    """
    Возвращает данные для получения JWT токена

    Args:
        user (User): Пользователь

    Returns:
        dict: Данные для получения токена
    """
    return {
        'email': user.email,
        'password': 'testpass123'  # Предполагаем, что пароль известен
    }


def get_invalid_token_data():
    """
    Возвращает невалидные данные для получения JWT токена

    Returns:
        dict: Невалидные данные для токена
    """
    return {
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }
