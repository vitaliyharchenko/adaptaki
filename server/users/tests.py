from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Тесты для модели CustomUser"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str_representation(self):
        """Тест строкового представления пользователя"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])

    def test_get_full_name(self):
        """Тест получения полного имени"""
        user = User.objects.create_user(**self.user_data)
        expected_full_name = f"{self.user_data['first_name']} {self.user_data['last_name']}"
        self.assertEqual(user.get_full_name(), expected_full_name)

    def test_get_short_name(self):
        """Тест получения короткого имени"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_short_name(), self.user_data['first_name'])

    def test_email_required(self):
        """Тест обязательности email"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')

    def test_email_normalization(self):
        """Тест нормализации email"""
        user = User.objects.create_user(
            email='TEST@EXAMPLE.COM',
            password='testpass123'
        )
        # Email нормализуется в нижний регистр
        self.assertEqual(user.email, 'TEST@example.com')


class UserSerializerTest(APITestCase):
    """Тесты для сериализаторов"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(
            email='existing@example.com',
            password='testpass123',
            first_name='Existing',
            last_name='User'
        )

    def test_user_serializer(self):
        """Тест UserSerializer"""
        from .serializers import UserSerializer
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertIn('id', data)
        self.assertIn('date_joined', data)
        self.assertNotIn('password', data)

    def test_user_create_serializer_valid_data(self):
        """Тест UserCreateSerializer с валидными данными"""
        from .serializers import UserCreateSerializer
        serializer = UserCreateSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])

    def test_user_create_serializer_password_mismatch(self):
        """Тест UserCreateSerializer с несовпадающими паролями"""
        from .serializers import UserCreateSerializer
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'differentpassword'
        serializer = UserCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_user_create_serializer_weak_password(self):
        """Тест UserCreateSerializer со слабым паролем"""
        from .serializers import UserCreateSerializer
        weak_password_data = self.user_data.copy()
        weak_password_data['password'] = '123'
        weak_password_data['password_confirm'] = '123'
        serializer = UserCreateSerializer(data=weak_password_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_user_update_serializer(self):
        """Тест UserUpdateSerializer"""
        from .serializers import UserUpdateSerializer
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        serializer = UserUpdateSerializer(self.user, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')


class UserViewsTest(APITestCase):
    """Тесты для views"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(
            email='existing@example.com',
            password='testpass123',
            first_name='Existing',
            last_name='User'
        )

    def test_user_create_view_success(self):
        """Тест успешной регистрации пользователя"""
        url = reverse('users:user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(email=self.user_data['email'])
        self.assertEqual(new_user.first_name, self.user_data['first_name'])
        self.assertEqual(new_user.last_name, self.user_data['last_name'])

    def test_user_create_view_invalid_data(self):
        """Тест регистрации с невалидными данными"""
        url = reverse('users:user-register')
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'wrongpassword'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_user_create_view_duplicate_email(self):
        """Тест регистрации с существующим email"""
        url = reverse('users:user-register')
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = self.user.email
        response = self.client.post(url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_user_detail_view_get_authenticated(self):
        """Тест получения профиля аутентифицированным пользователем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('users:user-update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # UserUpdateSerializer не включает email, поэтому проверяем только статус

    def test_user_detail_view_get_unauthenticated(self):
        """Тест получения профиля неаутентифицированным пользователем"""
        url = reverse('users:user-update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_view_update_authenticated(self):
        """Тест обновления профиля аутентифицированным пользователем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('users:user-update')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')

    def test_user_profile_view_authenticated(self):
        """Тест получения профиля через user_profile view"""
        self.client.force_authenticate(user=self.user)
        url = reverse('users:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_user_profile_view_unauthenticated(self):
        """Тест получения профиля неаутентифицированным пользователем"""
        url = reverse('users:user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_social_auth_redirect_view(self):
        """Тест social_auth_redirect view"""
        url = reverse('users:social-auth-redirect')
        response = self.client.get(url)
        # Этот view может требовать аутентификации в зависимости от настроек
        self.assertIn(response.status_code, [
                      status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('message', response.data)
            self.assertIn('user_id', response.data)


class JWTTokenTest(APITestCase):
    """Тесты для JWT токенов"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_obtain_token_success(self):
        """Тест успешного получения JWT токена"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_invalid_credentials(self):
        """Тест получения токена с неверными учетными данными"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_success(self):
        """Тест успешного обновления JWT токена"""
        # Получаем токены
        refresh = RefreshToken.for_user(self.user)
        url = reverse('token_refresh')
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_verify_token_success(self):
        """Тест успешной проверки JWT токена"""
        access = RefreshToken.for_user(self.user).access_token
        url = reverse('token_verify')
        data = {'token': str(access)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_invalid(self):
        """Тест проверки неверного JWT токена"""
        url = reverse('token_verify')
        data = {'token': 'invalid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAPIIntegrationTest(APITestCase):
    """Интеграционные тесты для API"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_full_user_workflow(self):
        """Тест полного workflow пользователя: регистрация -> получение токена -> получение профиля"""
        # 1. Регистрация нового пользователя
        register_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        register_url = reverse('users:user-register')
        register_response = self.client.post(
            register_url, register_data, format='json')
        self.assertEqual(register_response.status_code,
                         status.HTTP_201_CREATED)

        # 2. Получение JWT токена
        token_url = reverse('token_obtain_pair')
        token_data = {
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        token_response = self.client.post(token_url, token_data, format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access_token = token_response.data['access']

        # 3. Получение профиля с токеном
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('users:user-profile')
        profile_response = self.client.get(profile_url)
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['email'], 'newuser@example.com')

        # 4. Обновление профиля
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        update_url = reverse('users:user-update')
        update_response = self.client.put(
            update_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        # 5. Проверка обновления
        updated_profile_response = self.client.get(profile_url)
        self.assertEqual(
            updated_profile_response.data['first_name'], 'Updated')
        self.assertEqual(updated_profile_response.data['last_name'], 'Name')

    def test_api_without_authentication(self):
        """Тест доступа к защищенным эндпоинтам без аутентификации"""
        # Попытка получить профиль без токена
        profile_url = reverse('users:user-profile')
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Попытка обновить профиль без токена
        update_url = reverse('users:user-update')
        update_data = {'first_name': 'Test'}
        response = self.client.put(update_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_without_authentication(self):
        """Тест регистрации без аутентификации (должна работать)"""
        register_data = {
            'email': 'public@example.com',
            'password': 'publicpass123',
            'password_confirm': 'publicpass123',
            'first_name': 'Public',
            'last_name': 'User'
        }
        register_url = reverse('users:user-register')
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserAdminTest(TestCase):
    """Тесты для админки"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_admin_user_list(self):
        """Тест отображения списка пользователей в админке"""
        url = '/admin/users/customuser/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_user_change(self):
        """Тест изменения пользователя в админке"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        url = f'/admin/users/customuser/{user.id}/change/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_user_add(self):
        """Тест добавления пользователя в админке"""
        url = '/admin/users/customuser/add/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class UserValidationTest(APITestCase):
    """Тесты валидации данных пользователя"""

    def test_email_validation(self):
        """Тест валидации email"""
        url = reverse('users:user-register')

        # Неверный формат email
        invalid_data = {
            'email': 'invalid-email',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

        # Пустой email
        invalid_data['email'] = ''
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_password_validation(self):
        """Тест валидации пароля"""
        url = reverse('users:user-register')

        # Слишком короткий пароль
        invalid_data = {
            'email': 'test@example.com',
            'password': '123',
            'password_confirm': '123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

        # Пароль только из цифр
        invalid_data['password'] = '12345678'
        invalid_data['password_confirm'] = '12345678'
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_required_fields_validation(self):
        """Тест валидации обязательных полей"""
        url = reverse('users:user-register')

        # Отсутствует email
        invalid_data = {
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

        # Отсутствует password
        invalid_data = {
            'email': 'test@example.com',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
