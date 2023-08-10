# Запуск проекта

-   с venv `source env/bin/activate`
-   c docker `docker compose up`

# Что сделано

-   [x] Создана модель пользователя, к которой привязан идентефикатор телефоном и телеграмом
-   [x] Создана модель Question
-   [x] Созданы модели для графа
-   [x] Перенесена база заданий, тегов
-   [x] Подготовлен архив файлов со старого сервера
-   [x] Запущен API для получения заданий по id
-   [x] Запущен API для получения экзаменационного дерева
-   [x] Добавить поддержку математики в markdownx поля в админке
-   [x] Научиться проверять ответ и выставлять баллы
-   [x] Добавить в админку django-autocomplete для сложных полей (концепт, тег экзамена, sen)
-   [x] Закрыть ответами все задания на выбор с нулем верных `python manage.py find_zero_answers questions`
-   [x] Разобраться с тегами экзамена без привязки экзамена и номера
-   [x] Научиться детектировать пользователя по запросу к API для хранения результата
-   [x] Научиться регистрировать нового пользователя из бота
-   [x] Научиться выдавать токены по telegram_id
-   [x] Научиться определять пользователя по токену (просто `request.user` в APIview)
-   [x] Подключить нормальную базу данных

# todo

-   [] Отрендерить вариант ыответа на вопросы
    -   [] Добавить поле с номером варианта (1234) и перемешать существующие опции рандомно
    -   [] Научиться проверять ответ не в виде массива pk опций, а в виде 1234
-   [] Добавить максимальные баллы в sen
-   [] Научиться собирать результаты ученика по se, sen, exam_tag
-   [] Научиться предсказывать результат ребенка на экзамене (se)
    -   собираем последние три решенных задачи по каждому номеру
    -   если недостаточно данных, пишем, какие задания нужно дорешать
    -   считаем среднее по номеру с упором на последние (3*r1+2*r2+r3/6)
    -   суммируем средние и максимальные баллы
-   [] Закрыть задачами все вершины без задач `python manage.py classify_nodes graph`
-   [] Перенести картинки в условие задачи
-   [] Уменьшить сборку TexLive (https://packages.debian.org/search?keywords=texlive)

# забавно

-   В базе sqlite3 невозможно сделать поиск по полям в админке case insensitive
-   Существует API для доступа к РЕшуЕГЭ (https://github.com/anijackich/sdamgia-api)

# составляющие проекта

## сервер

-   Docker
    -   nginx
    -   web (Python)
        -   Django
        -   rest-framework
    -   postgres

## Docker

-   https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django/
-   https://www.geeksforgeeks.org/how-to-dockerize-django-application-for-production-deployement-with-gunicorn-and-nginx/
-   https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

## Django

Django, being a web framework, needs a web server in order to operate
Выбор упал на WSGI, асинхронность сейчас не важна

WSGI servers:

-   Gunicorn - написан на питоне и не требует зависимостей
-   uWSGI

Staticfiles Storage

-   FileSystemStorage class implements basic file storage on a local filesystem (наш выбор, статики не так уж и много)

## бот

-   Выбор технологии:
    -   aiogram (асинхронная с русским комьюнити)
    -   python-telegram-bot (синхронная, ждет ответа пользователя в любом случае)
