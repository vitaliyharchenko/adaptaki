# Приложение Users

Django приложение для управления пользователями с кастомной моделью, JWT-аутентификацией и социальной авторизацией.

## Описание

Приложение `users` предоставляет полную систему аутентификации и авторизации с кастомной моделью пользователя, которая использует email в качестве основного идентификатора.

## Возможности

-   ✅ Кастомная модель пользователя с email в качестве USERNAME_FIELD
-   ✅ Django REST Framework с JWT-аутентификацией
-   ✅ Авторизация через Google OAuth2
-   ✅ Авторизация через VK OAuth2
-   ✅ API эндпоинты для регистрации и управления профилем
-   ✅ Админка Django с кастомной моделью пользователя

## Структура файлов

```
users/
├── __init__.py
├── admin.py              # Регистрация модели в админке
├── apps.py               # Конфигурация приложения
├── migrations/           # Миграции базы данных
│   └── 0001_initial.py  # Начальная миграция
├── models.py             # Кастомная модель пользователя
├── serializers.py        # DRF сериализаторы
├── urls.py               # URL маршруты
├── views.py              # API views
└── README.md             # Этот файл
```

## Модели

### CustomUser

Кастомная модель пользователя, наследуется от `AbstractBaseUser` и `PermissionsMixin`.

#### Поля:

-   `email` - Email адрес (уникальный, основной идентификатор)
-   `first_name` - Имя пользователя
-   `last_name` - Фамилия пользователя
-   `is_staff` - Статус персонала (доступ к админке)
-   `is_active` - Активен ли пользователь
-   `date_joined` - Дата регистрации
-   `groups` - Группы пользователя (наследуется от PermissionsMixin)
-   `user_permissions` - Права пользователя (наследуется от PermissionsMixin)

#### Методы:

-   `get_full_name()` - Полное имя пользователя
-   `get_short_name()` - Короткое имя пользователя
-   `__str__()` - Строковое представление (email)

### CustomUserManager

Кастомный менеджер для создания пользователей.

#### Методы:

-   `create_user(email, password=None, **extra_fields)` - Создание обычного пользователя
-   `create_superuser(email, password=None, **extra_fields)` - Создание суперпользователя

## Сериализаторы

### UserSerializer

Сериализатор для отображения информации о пользователе.

**Поля:** `id`, `email`, `first_name`, `last_name`, `date_joined`
**Только для чтения:** `id`, `date_joined`

### UserCreateSerializer

Сериализатор для регистрации нового пользователя.

**Поля:** `email`, `first_name`, `last_name`, `password`, `password_confirm`
**Валидация:** Проверка совпадения паролей, валидация сложности пароля

### UserUpdateSerializer

Сериализатор для обновления профиля пользователя.

**Поля:** `first_name`, `last_name`

## Views

### UserCreateView

**Класс:** `generics.CreateAPIView`
**URL:** `/api/users/register/`
**Метод:** POST
**Разрешения:** `AllowAny`
**Описание:** Регистрация нового пользователя

### UserDetailView

**Класс:** `generics.RetrieveUpdateAPIView`
**URL:** `/api/users/profile/update/`
**Метод:** GET, PUT
**Разрешения:** `IsAuthenticated`
**Описание:** Получение и обновление профиля текущего пользователя

### user_profile

**Функция:** `@api_view(['GET'])`
**URL:** `/api/users/profile/`
**Метод:** GET
**Разрешения:** `IsAuthenticated`
**Описание:** Получение профиля текущего пользователя

### social_auth_redirect

**Функция:** `@api_view(['GET'])`
**URL:** `/api/users/social-auth-redirect/`
**Метод:** GET
**Разрешения:** Любые
**Описание:** Редирект после успешной социальной аутентификации

## URL маршруты

```python
urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/update/', views.UserDetailView.as_view(), name='user-update'),
    path('social-auth-redirect/', views.social_auth_redirect, name='social-auth-redirect'),
]
```

## Админка

### CustomUserAdmin

Кастомная админка для модели `CustomUser`.

**Отображение в списке:** `email`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`
**Фильтры:** `is_staff`, `is_active`, `date_joined`
**Поиск:** `email`, `first_name`, `last_name`
**Сортировка:** по `email`

**Наборы полей:**

-   Основная информация: `email`, `password`
-   Персональная информация: `first_name`, `last_name`
-   Разрешения: `is_active`, `is_staff`, `is_superuser`, `groups`, `user_permissions`
-   Важные даты: `last_login`, `date_joined`

## Миграции

### 0001_initial.py

Начальная миграция для создания таблицы `users_customuser` с полной структурой кастомной модели пользователя.

## Настройки в settings.py

### AUTH_USER_MODEL

```python
AUTH_USER_MODEL = 'users.CustomUser'
```

### REST_FRAMEWORK

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### JWT настройки

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

### Социальная аутентификация

```python
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH2_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('VK_OAUTH2_KEY', '')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('VK_OAUTH2_SECRET', '')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']
```

## API эндпоинты

### Регистрация пользователя

```http
POST /api/users/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Иван",
    "last_name": "Иванов"
}
```

### Получение JWT токена

```http
POST /api/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

### Получение профиля

```http
GET /api/users/profile/
Authorization: Bearer <jwt_token>
```

### Обновление профиля

```http
PUT /api/users/profile/update/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "first_name": "Новое имя",
    "last_name": "Новая фамилия"
}
```

## Тестирование

### Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

### Тестирование API

```bash
# Регистрация
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","password_confirm":"testpass123","first_name":"Test","last_name":"User"}'

# Получение токена
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Получение профиля
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <jwt_token>"
```

## Зависимости

-   `djangorestframework` - Django REST Framework
-   `djangorestframework-simplejwt` - JWT аутентификация
-   `social-auth-app-django` - Социальная аутентификация

## Переменные окружения

Для работы социальной аутентификации необходимо настроить в `.env`:

```env
GOOGLE_OAUTH2_KEY=your-google-oauth2-key
GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
VK_OAUTH2_KEY=your-vk-oauth2-key
VK_OAUTH2_SECRET=your-vk-oauth2-secret
```

## Безопасность

-   Пароли валидируются с помощью Django password validators
-   JWT токены имеют ограниченное время жизни
-   Все API эндпоинты (кроме регистрации) требуют аутентификации
-   Социальная аутентификация использует OAuth2 протокол

## Тестирование

Приложение полностью покрыто тестами (50 тестов). Подробная информация в файле [TEST_README.md](TEST_README.md).

### Быстрый запуск тестов:

```bash
# Все тесты
docker-compose exec web python manage.py test users -v 2

# Только упрощенные тесты
docker-compose exec web python manage.py test users.test_simple -v 2

# Конкретный тип тестов
docker-compose exec web python manage.py test users.tests.CustomUserModelTest -v 2
```

### Особенности тестирования:

-   ✅ Используется тестовая in-memory база данных
-   ✅ Автоматическая очистка после каждого теста
-   ✅ Фикстуры для переиспользования тестовых данных
-   ✅ 100% покрытие всех компонентов
-   ✅ Интеграционные тесты полного workflow
