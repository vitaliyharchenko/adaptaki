# Adaptaki - Django проект с кастомной аутентификацией

## Описание

Django проект с кастомной моделью пользователя, DRF, JWT-аутентификацией и авторизацией через социальные сети.

## Возможности

-   ✅ Кастомная модель пользователя с email в качестве USERNAME_FIELD
-   ✅ Django REST Framework с JWT-аутентификацией
-   ✅ Авторизация через Google OAuth2
-   ✅ Авторизация через VK OAuth2
-   ✅ API эндпоинты для регистрации и управления профилем
-   ✅ Docker Compose для развертывания

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd adaptaki
cp env.example .env
```

### 2. Настройка переменных окружения

Отредактируйте файл `.env`:

```env
# Database configuration (PostgreSQL)
POSTGRES_DB=adaptaki
POSTGRES_USER=adaptaki
POSTGRES_PASSWORD=adaptaki
DB_HOST=db
DB_PORT=5432

# Django settings
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1,http://localhost

# Social Auth settings
GOOGLE_OAUTH2_KEY=your-google-oauth2-key
GOOGLE_OAUTH2_SECRET=your-google-oauth2-secret
VK_OAUTH2_KEY=your-vk-oauth2-key
VK_OAUTH2_SECRET=your-vk-oauth2-secret
```

### 3. Запуск с Docker Compose

```bash
docker-compose up -d
```

### 4. Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

## API Эндпоинты

### JWT Аутентификация

-   `POST /api/token/` - Получение JWT токенов
-   `POST /api/token/refresh/` - Обновление JWT токена
-   `POST /api/token/verify/` - Проверка JWT токена

### Пользователи

-   `POST /api/users/register/` - Регистрация нового пользователя
-   `GET /api/users/profile/` - Получение профиля пользователя
-   `PUT /api/users/profile/update/` - Обновление профиля пользователя

### Социальная аутентификация

-   `GET /social-auth/login/google-oauth2/` - Вход через Google
-   `GET /social-auth/login/vk-oauth2/` - Вход через VK
-   `GET /api/users/social-auth-redirect/` - Редирект после социальной аутентификации

## Настройка социальной аутентификации

### Google OAuth2

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте новый проект или выберите существующий
3. Включите Google+ API
4. Создайте OAuth 2.0 credentials
5. Добавьте разрешенные URI перенаправления:
    - `http://localhost:8000/social-auth/complete/google-oauth2/`
6. Скопируйте Client ID и Client Secret в `.env`

### VK OAuth2

1. Перейдите в [VK Developers](https://vk.com/dev)
2. Создайте новое приложение
3. В настройках приложения укажите:
    - Site URL: `http://localhost:8000`
    - Base domain: `localhost`
4. Скопируйте Application ID и Secure Key в `.env`

## Структура проекта

```
adaptaki/
├── docker-compose.yml
├── env.example
├── README.md
└── server/
    ├── conf/
    │   ├── settings.py
    │   └── urls.py
    ├── users/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── admin.py
    ├── requirements.txt
    └── manage.py
```

## Модель пользователя

Кастомная модель `CustomUser` наследуется от `AbstractBaseUser` и `PermissionsMixin`:

-   `email` - основной идентификатор пользователя
-   `first_name`, `last_name` - имя и фамилия
-   `is_staff`, `is_active` - статусы пользователя
-   `date_joined` - дата регистрации

## Разработка

### Локальная разработка

```bash
# Активация виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r server/requirements.txt

# Применение миграций
python server/manage.py migrate

# Запуск сервера разработки
python server/manage.py runserver
```

### Тестирование API

```bash
# Регистрация пользователя
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","password_confirm":"testpass123","first_name":"Test","last_name":"User"}'

# Получение JWT токена
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Получение профиля (с токеном)
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Лицензия

MIT License
