# adaptaki

## Инфраструктура

Яндекс Виртуальная машина с доступом по ssh
`ssh vitaliyharchenko@89.169.182.234`
Туда установлен `docker-compose version 1.29.2`

## TODO

-   [x] Создал виртуальную машину на Яндекс облако и хранилище для файловъ
-   [x] Запустил проект с docker-compose локально
-   [ ] Проверить почту

## Запуск проекта (Docker Compose)

### Локальная разработка

1. Создайте файл окружения из примера:
    - macOS/Linux: `cp env.example .env`
    - Windows PowerShell: `Copy-Item env.example .env`
2. Для разработки включите DEBUG в `.env`:
    - `DJANGO_DEBUG=1`
3. Соберите и запустите сервисы:
    - `docker compose up -d --build`
4. Приложение доступно по адресу: `http://127.0.0.1:8000/`
5. Остановка и очистка:
    - `docker compose down -v`

### Продакшен

1. Создайте файл окружения из примера:
    - `cp env.example .env`
2. Настройте продакшен переменные в `.env`:
    - `DJANGO_DEBUG=0`
    - `DJANGO_SECRET_KEY=<strong-secret>`
    - `DJANGO_ALLOWED_HOSTS=<your-domain>,localhost`
    - `DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-domain>,http://localhost`
3. Соберите и запустите сервисы:
    - `docker compose up -d --build`

Сервис `web` автоматически выполнит миграции и collectstatic перед стартом, работает через gunicorn. База данных — контейнер `db` (PostgreSQL 15). По умолчанию слушает `127.0.0.1:8000` (для работы за Nginx на сервере).

## Переменные окружения

Смотрите `env.example` для примера настроек PostgreSQL и Django. Ключевые параметры:

-   `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_HOST`, `DB_PORT`
-   `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`

**Важно**: Для продакшена обязательно установите `DJANGO_DEBUG=0` и надёжный `DJANGO_SECRET_KEY`.

## Деплой на сервер (ручной)

1. Подключиться по SSH:
    - `ssh vitaliyharchenko@89.169.182.234`
2. Установить git (если нет):
    - Ubuntu/Debian: `sudo apt update && sudo apt install -y git`
3. Клонировать репозиторий (первый раз):
    - `git clone https://github.com/vitaliyharchenko/adaptaki.git && cd adaptaki`
    - далее: `git pull`
4. Создать `.env` на сервере (на основе `env.example`) с прод-настройками:
    - `DJANGO_DEBUG=0`
    - `DJANGO_ALLOWED_HOSTS=89.169.182.234,localhost`
    - `DJANGO_CSRF_TRUSTED_ORIGINS=http://89.169.182.234,http://localhost`
    - замените пароли на надёжные.
5. Запуск:
    - `docker compose up -d --build`
6. Проверка:
    - за Nginx: открыть домен проекта по HTTPS (рекомендуется)
    - без Nginx (временно): опубликовать порт как `8000:8000` и открыть `http://<IP>:8000/`

Примечание: убедитесь, что в правилах фаервола (безопасности) Яндекс.Облака открыт TCP-порт 8000, либо настройте обратный прокси (nginx) на 80/443.

## CI/CD через GitHub Actions (деплой по SSH)

1. Добавьте секреты репозитория:
    - `SSH_HOST=89.169.182.234`
    - `SSH_USER=vitaliyharchenko`
    - `SSH_KEY` — приватный ключ (PEM) пользователя для доступа к ВМ
2. Workflow запускается на `push` в `main`: он подключается по SSH к серверу, делает `git pull` и `docker compose up -d --build`.

## Примечания

-   Для продакшена выключайте DEBUG и задавайте надёжный `DJANGO_SECRET_KEY`.
-   Проект использует PostgreSQL в Docker Compose для всех окружений.
-   Health‑эндпоинт доступен по адресу `/healthz/` для мониторинга.

### Конспект: что мы настроили и как деплоить

-   **Инфраструктура**: ВМ в Яндекс.Облаке со статическим IP и доступом по SSH. Установлен Docker и Docker Compose V2 (команда `docker compose`).
-   **Проект (backend)**: Django 5 + PostgreSQL. Перевели конфиг на переменные окружения (`DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`). Добавили `gunicorn` и `whitenoise` для продакшна.
-   **Docker Compose**: Сервис `web` (gunicorn, авто `migrate` и `collectstatic`) и `db` (Postgres 15). В проде `web` слушает `127.0.0.1:8000` (за Nginx). Health‑эндпоинт `/healthz/` для мониторинга.
-   **Локальный запуск**: `cp env.example .env` → `DJANGO_DEBUG=1` → `docker compose up -d --build` → http://127.0.0.1:8000
-   **ВМ — первый запуск**:
    -   Клонировать репозиторий, создать `.env` (в проде `DJANGO_DEBUG=0`, добавить IP/домен в `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS`).
    -   Запустить: `docker compose up -d --build`.
-   **CI/CD (GitHub Actions)**: Добавлен workflow `.github/workflows/deploy.yml` — деплой по SSH на ВМ при `push` в `main`.
    -   Секреты репозитория: `SSH_HOST`, `SSH_USER`, `SSH_KEY` (приватный ключ для входа на ВМ).
-   **Сеть и безопасность**: Открыть в Группе безопасности порты 8000 (или 80/443 при Nginx). При включённом UFW: `sudo ufw allow 8000/tcp` или `sudo ufw allow 80,443/tcp`.
-   **Проверка доступности**:
    -   На ВМ: `curl -I http://127.0.0.1:8000` и `docker compose logs --tail=100 web`.
    -   Снаружи: через домен/HTTPS за Nginx.
-   **Домены и HTTPS (рекомендуется)** для поддомена `server.adaptaki.ru`:
    -   DNS: A-запись `server → <IP>`.
    -   Nginx reverse proxy на ВМ (проксировать на `http://127.0.0.1:8000`).
    -   Let's Encrypt: `certbot --nginx -d server.adaptaki.ru --redirect -m <email> --agree-tos -n`.
-   **Частые проблемы**:
    -   `permission denied /var/run/docker.sock`: добавить пользователя в группу `docker` (`sudo usermod -aG docker $USER`, затем `newgrp docker`/перелогин).
    -   `400 Bad Request (DisallowedHost)`: добавить IP/домен в `DJANGO_ALLOWED_HOSTS` и `DJANGO_CSRF_TRUSTED_ORIGINS` и перезапустить.
    -   `Permission denied (publickey)` при `git push`: настроить SSH‑ключ и `~/.ssh/config` для `github.com`.
