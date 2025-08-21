# adaptaki

## Инфраструктура

Яндекс Виртуальная машина с доступом по ssh
`ssh vitaliyharchenko@89.169.182.234`
Туда установлен `docker-compose version 1.29.2`

## TODO

-   [x] Создал виртуальную машину на Яндекс облако и хранилище для файловъ
-   [x] Запустил проект с .venv локально
-   [x] Запустил проект с docker-compose локально
-   [ ] Проверить почту

## Запуск локально (без Docker)

1. Создайте и активируйте виртуальное окружение:
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
2. Установите зависимости:
    - `pip install -r server/requirements.txt`
3. Примените миграции и запустите dev-сервер:
    - `python server/manage.py migrate`
    - `python server/manage.py runserver`
4. Откройте: `http://127.0.0.1:8000/`

## Запуск через Docker Compose (PostgreSQL)

1. Создайте файл окружения из примера:
    - macOS/Linux: `cp env.example .env`
    - Windows PowerShell: `Copy-Item env.example .env`
2. Соберите и запустите сервисы:
    - `docker compose up -d --build`
3. Приложение доступно по адресу: `http://127.0.0.1:8000/`
4. Остановка и очистка:
    - `docker compose down -v`

Сервис `web` автоматически выполнит миграции перед стартом. База данных — контейнер `db` (PostgreSQL 15) с healthcheck.

## Переменные окружения

Смотрите `env.example` для примера настроек PostgreSQL и Django. Ключевые параметры:

-   `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
-   `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
-   `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`

## Примечания

-   В режиме без Docker `server/conf/settings.py` автоматически использует SQLite при отсутствии `POSTGRES_*`/`DB_*`.
-   Для продакшна выключайте DEBUG и задавайте надёжный `DJANGO_SECRET_KEY`.
