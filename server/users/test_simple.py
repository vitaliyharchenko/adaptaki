"""
Упрощенные тесты с использованием фикстур
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .fixtures import (
    create_test_user, create_test_superuser, get_authenticated_client,
    get_token_authenticated_client, get_valid_user_data, get_invalid_user_data,
    get_update_user_data, get_token_data, get_invalid_token_data
)


class SimpleUserModelTest(TestCase):
    """Упрощенные тесты модели пользователя"""

    def test_create_user_with_fixture(self):
        """Тест создания пользователя с помощью фикстуры"""
        user = create_test_user()
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser_with_fixture(self):
        """Тест создания суперпользователя с помощью фикстуры"""
        admin = create_test_superuser()
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_create_user_with_custom_data(self):
        """Тест создания пользователя с кастомными данными"""
        user = create_test_user(
            email='custom@example.com',
            first_name='Custom',
            last_name='Name'
        )
        self.assertEqual(user.email, 'custom@example.com')
        self.assertEqual(user.first_name, 'Custom')
        self.assertEqual(user.last_name, 'Name')


class SimpleAPIViewTest(APITestCase):
    """Упрощенные тесты API views"""

    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя"""
        url = reverse('users:user-register')
        data = get_valid_user_data()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_failure(self):
        """Тест неудачной регистрации пользователя"""
        url = reverse('users:user-register')
        data = get_invalid_user_data()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_profile_authenticated(self):
        """Тест получения профиля аутентифицированным пользователем"""
        user = create_test_user()
        client = get_authenticated_client(user)
        url = reverse('users:user-profile')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)

    def test_get_profile_unauthenticated(self):
        """Тест получения профиля неаутентифицированным пользователем"""
        url = reverse('users:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile_authenticated(self):
        """Тест обновления профиля аутентифицированным пользователем"""
        user = create_test_user()
        client = get_authenticated_client(user)
        url = reverse('users:user-update')
        data = get_update_user_data()
        response = client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_unauthenticated(self):
        """Тест обновления профиля неаутентифицированным пользователем"""
        url = reverse('users:user-update')
        data = get_update_user_data()
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SimpleJWTTest(APITestCase):
    """Упрощенные тесты JWT"""

    def test_obtain_token_success(self):
        """Тест успешного получения JWT токена"""
        user = create_test_user()
        url = reverse('token_obtain_pair')
        data = get_token_data(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_failure(self):
        """Тест неудачного получения JWT токена"""
        url = reverse('token_obtain_pair')
        data = get_invalid_token_data()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_token(self):
        """Тест доступа с JWT токеном"""
        user = create_test_user()
        client, access_token = get_token_authenticated_client(user)
        url = reverse('users:user-profile')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SimpleIntegrationTest(APITestCase):
    """Упрощенные интеграционные тесты"""

    def test_full_user_workflow(self):
        """Тест полного workflow пользователя"""
        # 1. Регистрация
        register_data = get_valid_user_data()
        register_url = reverse('users:user-register')
        register_response = self.client.post(
            register_url, register_data, format='json')
        self.assertEqual(register_response.status_code,
                         status.HTTP_201_CREATED)

        # 2. Получение токена
        token_url = reverse('token_obtain_pair')
        token_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        token_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access_token = token_response.data['access']

        # 3. Доступ к защищенному эндпоинту
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('users:user-profile')
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)

    def test_duplicate_email_registration(self):
        """Тест регистрации с дублирующимся email"""
        # Создаем первого пользователя
        user = create_test_user()

        # Пытаемся создать второго с тем же email
        register_data = get_valid_user_data()
        register_data['email'] = user.email
        register_url = reverse('users:user-register')
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class SimpleAdminTest(TestCase):
    """Упрощенные тесты админки"""

    def test_admin_access(self):
        """Тест доступа к админке"""
        admin = create_test_superuser()
        self.client.force_login(admin)

        # Тест списка пользователей
        url = '/admin/users/customuser/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Тест добавления пользователя
        url = '/admin/users/customuser/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
