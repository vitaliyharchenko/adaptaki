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

### Граф знаний (Graph API)

-   `GET /api/graph/subjects/` - Получение списка предметов
-   `POST /api/graph/subjects/` - Создание нового предмета
-   `GET /api/graph/concepts/` - Получение списка концептов
-   `POST /api/graph/concepts/` - Создание нового концепта
-   `GET /api/graph/nodes/` - Получение списка узлов графа
-   `POST /api/graph/nodes/` - Создание нового узла
-   `GET /api/graph/node-relations/` - Получение списка связей между узлами
-   `POST /api/graph/node-relations/` - Создание новой связи

**Фильтрация для узлов:**

-   `GET /api/graph/nodes/?subject=1` - Фильтр по предмету
-   `GET /api/graph/nodes/?concept=1` - Фильтр по концепту
-   `GET /api/graph/nodes/?search=квадрат` - Поиск по названию

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
    ├── graph/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── admin.py
    ├── requirements.txt
    └── manage.py
```

## Модели

### Модель пользователя

Кастомная модель `CustomUser` наследуется от `AbstractBaseUser` и `PermissionsMixin`:

-   `email` - основной идентификатор пользователя
-   `first_name`, `last_name` - имя и фамилия
-   `is_staff`, `is_active` - статусы пользователя
-   `date_joined` - дата регистрации

### Модели графа знаний

**Subject** - Предмет (физика, математика и т.д.):

-   `title` - название предмета

**Concept** - Большая тема, объединяющая несколько вершин:

-   `title` - название концепта
-   `subject` - связь с предметом
-   `is_active` - активен ли концепт

**Node** - Узел графа знаний:

-   `title` - название узла
-   `type` - тип узла (KN - понятие, UN - закономерность, CS - кейс, SK - навык)
-   `subject` - связь с предметом
-   `concept` - связь с концептом
-   `testability` - проверяемость узла

**NodeRelation** - Связь между узлами графа:

-   `parent` - родительский узел
-   `child` - дочерний узел

## Разработка

### Рекомендуемый способ разработки через Docker Compose

**Важно:** Все команды Django (создание приложений, миграции, создание суперпользователя и т.д.) должны выполняться через Docker Compose для обеспечения консистентности окружения.

```bash
# Создание нового Django приложения
docker-compose exec web python manage.py startapp myapp

# Применение миграций
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic

# Запуск shell
docker-compose exec web python manage.py shell
```

### Локальная разработка (альтернативный способ)

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

# Тестирование Graph API
curl -X GET http://localhost:8000/api/graph/subjects/ \
  -H "Authorization: Bearer <your-jwt-token>"

curl -X POST http://localhost:8000/api/graph/subjects/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"title":"Химия"}'
```

### Запуск тестов

```bash
# Запуск всех тестов
docker-compose exec web python manage.py test

# Запуск тестов конкретного приложения
docker-compose exec web python manage.py test users
docker-compose exec web python manage.py test graph

# Запуск конкретного теста
docker-compose exec web python manage.py test graph.tests.GraphModelsTest
```

## Лицензия

MIT License
