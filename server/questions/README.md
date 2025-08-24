# Приложение Questions

Приложение для создания и управления задачами и вопросами с поддержкой различных типов ответов.

## Модели

### Question

Основная модель задачи с поддержкой:

-   Условия задачи с CKEditor (картинки, формулы)
-   Разбора задачи
-   Различных типов ответов
-   Политик проверки
-   Связей с узлами графа знаний
-   Аналогичных задач

### QuestionOption

Варианты ответов для задач:

-   Текст с поддержкой CKEditor
-   Флаг правильности
-   Порядок отображения

## Типы заданий

1. **STRING** - Ответ строкой
2. **NUMBER** - Ответ числом
3. **SEQ_ORDERED** - Последовательность с порядком
4. **SEQ_UNORDERED** - Последовательность без порядка

## Политики проверки

1. **ALL_OR_NOTHING** - Все или ничего
2. **PER_ERROR** - За каждую ошибку -1 балл

## API Endpoints

### Основные операции

-   `GET /api/questions/questions/` - Список задач
-   `POST /api/questions/questions/` - Создание задачи
-   `GET /api/questions/questions/{id}/` - Детали задачи
-   `PUT /api/questions/questions/{id}/` - Обновление задачи
-   `DELETE /api/questions/questions/{id}/` - Удаление задачи

### Специальные операции

-   `POST /api/questions/questions/{id}/check_answer/` - Проверка ответа
-   `GET /api/questions/questions/{id}/get_random_analog/` - Случайная аналогичная задача
-   `GET /api/questions/questions/random_by_node/` - Случайная задача по узлу
-   `GET /api/questions/questions/statistics/` - Статистика
-   `POST /api/questions/questions/{id}/copy/` - Копирование задачи
-   `POST /api/questions/questions/{id}/add_analog/` - Добавление аналогичной задачи
-   `DELETE /api/questions/questions/{id}/remove_analog/` - Удаление аналогичной задачи

### Фильтрация и поиск

-   `?question_type=STRING` - По типу задания
-   `?is_active=true` - Только активные
-   `?node_id=1` - По узлу графа
-   `?subject_id=1` - По предмету
-   `?concept_id=1` - По концепту
-   `?search=текст` - Поиск по тексту
-   `?ordering=title` - Сортировка

## Примеры использования

### Создание задачи с вариантами ответов

```json
{
    "title": "Решите уравнение x² + 5x + 6 = 0",
    "condition": "<p>Найдите корни квадратного уравнения:</p><p>x² + 5x + 6 = 0</p>",
    "solution": "<p>Используя формулу дискриминанта...</p>",
    "question_type": "NUMBER",
    "max_score": 2,
    "grading_policy": "ALL_OR_NOTHING",
    "options": [
        { "text": "-2", "is_correct": true, "order": 1 },
        { "text": "-3", "is_correct": true, "order": 2 },
        { "text": "2", "is_correct": false, "order": 3 },
        { "text": "3", "is_correct": false, "order": 4 }
    ]
}
```

### Проверка ответа

```json
POST /api/questions/questions/1/check_answer/
{
  "answer": -2
}
```

Ответ:

```json
{
    "is_correct": true,
    "score": 2,
    "feedback": "Правильно!",
    "max_score": 2
}
```

## Админка

В админке доступны:

-   Создание и редактирование задач
-   Inline редактирование вариантов ответов
-   Копирование задач
-   Управление аналогичными задачами
-   Статистика по задачам

## Будущие возможности

Архитектура позволяет легко добавить:

-   Загрузку файлов (сочинения, фото)
-   Числа с заданной точностью
-   Заполнение пропусков
-   Упорядочивание элементов
-   Сопоставление столбцов
