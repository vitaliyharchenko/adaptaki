# Приложение Exams

Приложение для управления структурой экзаменов и олимпиад. Позволяет создавать иерархическую структуру рубрикатора экзаменов и привязывать к ним задачи.

## Описание

Приложение `exams` предназначено для организации структуры экзаменов по принципу:

1. **Экзамен** (ЕГЭ, ОГЭ, Олимпиада)
2. **Предмет** (Математика, Физика, Химия и т.д.)
3. **Номер задания** (Задание 1, Задание 2 и т.д.)
4. **Подтема** (Планиметрия, Стереометрия, Алгебра и т.д.)

Такая структура позволяет легко навигировать по экзаменам и находить нужные задачи, аналогично сайтам типа РЕшуЕГЭ.

## Модели данных

### ExamType

Типы экзаменов (ЕГЭ, ОГЭ, Олимпиада и т.д.)

**Поля:**

-   `name` - название экзамена
-   `description` - описание
-   `is_active` - активен ли экзамен
-   `order` - порядок отображения
-   `created_at`, `updated_at` - даты создания и обновления

### ExamSubject

Связь экзамена с предметом (использует существующую модель `Subject` из приложения `graph`)

**Поля:**

-   `exam_type` - тип экзамена (ForeignKey к ExamType)
-   `subject` - предмет (ForeignKey к graph.Subject)
-   `is_active` - активна ли связь
-   `order` - порядок отображения
-   `created_at`, `updated_at` - даты создания и обновления

### ExamNumber

Номера заданий в экзамене

**Поля:**

-   `exam_subject` - предмет экзамена (ForeignKey к ExamSubject)
-   `number` - номер задания (1-100)
-   `title` - название задания
-   `description` - описание
-   `is_active` - активно ли задание
-   `order` - порядок отображения
-   `created_at`, `updated_at` - даты создания и обновления

### ExamTopic

Подтемы внутри задания

**Поля:**

-   `exam_number` - номер задания (ForeignKey к ExamNumber)
-   `title` - название подтемы
-   `description` - описание
-   `is_active` - активна ли подтема
-   `order` - порядок отображения
-   `created_at`, `updated_at` - даты создания и обновления

## API Endpoints

### Основные endpoints

#### Типы экзаменов

-   `GET /api/exams/exam-types/` - список типов экзаменов
-   `POST /api/exams/exam-types/` - создать тип экзамена
-   `GET /api/exams/exam-types/{id}/` - получить тип экзамена
-   `PUT /api/exams/exam-types/{id}/` - обновить тип экзамена
-   `DELETE /api/exams/exam-types/{id}/` - удалить тип экзамена
-   `GET /api/exams/exam-types/{id}/subjects/` - получить предметы для экзамена

#### Предметы экзаменов

-   `GET /api/exams/exam-subjects/` - список предметов экзаменов
-   `POST /api/exams/exam-subjects/` - создать предмет экзамена
-   `GET /api/exams/exam-subjects/{id}/` - получить предмет экзамена
-   `PUT /api/exams/exam-subjects/{id}/` - обновить предмет экзамена
-   `DELETE /api/exams/exam-subjects/{id}/` - удалить предмет экзамена
-   `GET /api/exams/exam-subjects/{id}/numbers/` - получить номера заданий для предмета

#### Номера заданий

-   `GET /api/exams/exam-numbers/` - список номеров заданий
-   `POST /api/exams/exam-numbers/` - создать номер задания
-   `GET /api/exams/exam-numbers/{id}/` - получить номер задания
-   `PUT /api/exams/exam-numbers/{id}/` - обновить номер задания
-   `DELETE /api/exams/exam-numbers/{id}/` - удалить номер задания
-   `GET /api/exams/exam-numbers/{id}/topics/` - получить подтемы для номера задания

#### Подтемы экзаменов

-   `GET /api/exams/exam-topics/` - список подтем экзаменов
-   `POST /api/exams/exam-topics/` - создать подтему экзамена
-   `GET /api/exams/exam-topics/{id}/` - получить подтему экзамена
-   `PUT /api/exams/exam-topics/{id}/` - обновить подтему экзамена
-   `DELETE /api/exams/exam-topics/{id}/` - удалить подтему экзамена
-   `GET /api/exams/exam-topics/{id}/questions/` - получить задачи для подтемы

#### Навигация

-   `GET /api/exams/navigation/` - получить полную навигационную структуру

### Фильтрация и поиск

Все endpoints поддерживают:

-   **Фильтрацию** по полям `is_active` и связанным моделям
-   **Поиск** по названиям и описаниям
-   **Сортировку** по различным полям
-   **Пагинацию**

**Примеры запросов:**

```bash
# Получить только активные типы экзаменов
GET /api/exams/exam-types/?is_active=true

# Поиск по названию
GET /api/exams/exam-types/?search=ЕГЭ

# Сортировка по порядку
GET /api/exams/exam-types/?ordering=order

# Фильтрация предметов по типу экзамена
GET /api/exams/exam-subjects/?exam_type=1
```

## Интеграция с другими приложениями

### Связь с приложением Questions

Модель `Question` содержит поле:

```python
exam_topics = models.ManyToManyField(
    'exams.ExamTopic',
    blank=True,
    verbose_name='Подтемы экзаменов'
)
```

Это позволяет:

-   Привязывать задачи к конкретным подтемам экзаменов
-   Получать задачи по структуре экзаменов
-   Фильтровать задачи по экзаменам и предметам

### Связь с приложением Graph

Приложение использует существующую модель `Subject` из приложения `graph`:

```python
subject = models.ForeignKey(
    'graph.Subject',
    on_delete=models.CASCADE,
    verbose_name='Предмет'
)
```

Это обеспечивает:

-   Единообразие в названиях предметов
-   Связь с графом знаний
-   Возможность синхронизации структуры знаний с экзаменационной структурой

## Админка Django

Приложение предоставляет удобную админку для управления структурой экзаменов:

### Особенности админки:

-   **Иерархическое отображение** структуры экзаменов
-   **Inline редактирование** дочерних элементов
-   **Фильтры** по экзамену, предмету, активности
-   **Поиск** по названиям
-   **Счетчики** связанных элементов
-   **Сортировка** по порядку

### Доступные модели в админке:

-   `ExamTypeAdmin` - управление типами экзаменов
-   `ExamSubjectAdmin` - управление предметами экзаменов
-   `ExamNumberAdmin` - управление номерами заданий
-   `ExamTopicAdmin` - управление подтемами

## Методы моделей

### ExamType

-   `get_subjects()` - получить активные предметы для экзамена

### ExamSubject

-   `get_numbers()` - получить активные номера заданий для предмета

### ExamNumber

-   `get_topics()` - получить активные подтемы для номера задания
-   `get_full_path()` - получить полный путь к заданию

### ExamTopic

-   `get_questions()` - получить активные задачи для подтемы
-   `get_questions_count()` - получить количество задач для подтемы
-   `get_full_path()` - получить полный путь к подтеме

## Примеры использования

### Создание структуры экзамена

```python
# Создание типа экзамена
exam_type = ExamType.objects.create(
    name='ЕГЭ',
    description='Единый государственный экзамен',
    order=1
)

# Создание связи с предметом
exam_subject = ExamSubject.objects.create(
    exam_type=exam_type,
    subject=Subject.objects.get(title='Математика'),
    order=1
)

# Создание номера задания
exam_number = ExamNumber.objects.create(
    exam_subject=exam_subject,
    number=1,
    title='Планиметрия',
    description='Задачи на планиметрию',
    order=1
)

# Создание подтемы
exam_topic = ExamTopic.objects.create(
    exam_number=exam_number,
    title='Решение прямоугольного треугольника',
    description='Задачи на прямоугольные треугольники',
    order=1
)
```

### Получение задач по структуре экзамена

```python
# Получить все задачи для конкретной подтемы
topic = ExamTopic.objects.get(id=1)
questions = topic.get_questions()

# Получить количество задач
questions_count = topic.get_questions_count()

# Получить полный путь к подтеме
full_path = topic.get_full_path()
# Результат: "ЕГЭ → Математика → Задание 1 → Решение прямоугольного треугольника"
```

### API запросы

```python
import requests

# Получить полную навигационную структуру
response = requests.get('http://localhost:8000/api/exams/navigation/')
navigation = response.json()

# Получить предметы для ЕГЭ
response = requests.get('http://localhost:8000/api/exams/exam-types/1/subjects/')
subjects = response.json()

# Получить задачи для подтемы
response = requests.get('http://localhost:8000/api/exams/exam-topics/1/questions/')
questions = response.json()
```

## Миграции

Приложение включает миграции для создания всех необходимых таблиц:

```bash
# Создание миграций
python manage.py makemigrations exams

# Применение миграций
python manage.py migrate
```

## Тестирование

Для тестирования API можно использовать:

```bash
# Проверка работоспособности
python manage.py check

# Запуск тестов (если есть)
python manage.py test exams
```

## Будущие расширения

Возможные направления развития:

-   Версионирование структуры экзаменов
-   Статистика по рубрикам
-   Рекомендации задач по рубрикам
-   Экспорт/импорт структуры
-   Интеграция с внешними системами
-   Кэширование навигационной структуры
-   API для массового создания структуры
