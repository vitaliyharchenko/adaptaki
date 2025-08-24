# Graph - Приложение для управления графом знаний

## Описание

Приложение `graph` предназначено для создания и управления графом знаний в образовательной системе. Оно позволяет структурировать учебный материал в виде связанных концептов и узлов, что помогает выстраивать логические связи между различными темами и понятиями.

## Архитектура

Приложение построено на основе четырех основных моделей:

### 1. Subject (Предмет)
Базовый уровень организации знаний - учебный предмет (математика, физика, химия и т.д.).

**Поля:**
- `title` - название предмета (CharField, max_length=300)

### 2. Concept (Концепт)
Большая тема, объединяющая несколько связанных узлов в подграф. Например, "Квадратные уравнения" может включать узлы "Квадратное уравнение", "Дискриминант", "Формула корней".

**Поля:**
- `title` - название концепта (CharField, max_length=300)
- `subject` - связь с предметом (ForeignKey)
- `is_active` - активен ли концепт (BooleanField, default=False)

### 3. Node (Узел)
Отдельное понятие, закономерность, кейс или навык в графе знаний.

**Поля:**
- `title` - название узла (CharField, max_length=200)
- `type` - тип узла (CharField, choices):
  - `KN` - Понятие (знаю)
  - `UN` - Закономерность (понимаю)
  - `CS` - Кейс (наблюдаю)
  - `SK` - Навык (умею)
- `subject` - связь с предметом (ForeignKey)
- `concept` - связь с концептом (ForeignKey, optional)
- `testability` - проверяемость узла (BooleanField, default=True)

### 4. NodeRelation (Связь между узлами)
Определяет связи между узлами графа, создавая направленный граф знаний.

**Поля:**
- `parent` - родительский узел (ForeignKey)
- `child` - дочерний узел (ForeignKey)
- Ограничение уникальности: пара (parent, child) должна быть уникальной

## API Эндпоинты

### Предметы (Subjects)
- `GET /api/graph/subjects/` - получение списка предметов
- `POST /api/graph/subjects/` - создание нового предмета
- `GET /api/graph/subjects/{id}/` - получение конкретного предмета
- `PUT /api/graph/subjects/{id}/` - обновление предмета
- `DELETE /api/graph/subjects/{id}/` - удаление предмета

### Концепты (Concepts)
- `GET /api/graph/concepts/` - получение списка концептов
- `POST /api/graph/concepts/` - создание нового концепта
- `GET /api/graph/concepts/{id}/` - получение конкретного концепта
- `PUT /api/graph/concepts/{id}/` - обновление концепта
- `DELETE /api/graph/concepts/{id}/` - удаление концепта

### Узлы (Nodes)
- `GET /api/graph/nodes/` - получение списка узлов
- `POST /api/graph/nodes/` - создание нового узла
- `GET /api/graph/nodes/{id}/` - получение конкретного узла
- `PUT /api/graph/nodes/{id}/` - обновление узла
- `DELETE /api/graph/nodes/{id}/` - удаление узла

**Фильтрация и поиск:**
- `GET /api/graph/nodes/?subject=1` - фильтр по предмету
- `GET /api/graph/nodes/?concept=1` - фильтр по концепту
- `GET /api/graph/nodes/?search=квадрат` - поиск по названию

### Связи между узлами (NodeRelations)
- `GET /api/graph/node-relations/` - получение списка связей
- `POST /api/graph/node-relations/` - создание новой связи
- `GET /api/graph/node-relations/{id}/` - получение конкретной связи
- `PUT /api/graph/node-relations/{id}/` - обновление связи
- `DELETE /api/graph/node-relations/{id}/` - удаление связи

## Примеры использования

### Создание структуры знаний по математике

```python
# 1. Создание предмета
subject_data = {"title": "Математика"}
subject = requests.post('/api/graph/subjects/', json=subject_data)

# 2. Создание концепта
concept_data = {
    "title": "Квадратные уравнения",
    "subject": subject.json()['id'],
    "is_active": True
}
concept = requests.post('/api/graph/concepts/', json=concept_data)

# 3. Создание узлов
node1_data = {
    "title": "Квадратное уравнение",
    "type": "KN",
    "subject": subject.json()['id'],
    "concept": concept.json()['id'],
    "testability": True
}
node1 = requests.post('/api/graph/nodes/', json=node1_data)

node2_data = {
    "title": "Дискриминант",
    "type": "KN",
    "subject": subject.json()['id'],
    "concept": concept.json()['id'],
    "testability": True
}
node2 = requests.post('/api/graph/nodes/', json=node2_data)

# 4. Создание связи
relation_data = {
    "parent": node1.json()['id'],
    "child": node2.json()['id']
}
relation = requests.post('/api/graph/node-relations/', json=relation_data)
```

### Поиск узлов по предмету

```python
# Получение всех узлов по математике
nodes = requests.get('/api/graph/nodes/?subject=1')
print(f"Найдено узлов: {len(nodes.json()['results'])}")
```

### Поиск узлов по концепту

```python
# Получение всех узлов концепта "Квадратные уравнения"
nodes = requests.get('/api/graph/nodes/?concept=1')
print(f"Узлов в концепте: {len(nodes.json()['results'])}")
```

## Аутентификация

Все API эндпоинты требуют JWT-аутентификации. Для доступа к API необходимо:

1. Получить JWT токен:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

2. Использовать токен в заголовке:
```bash
curl -X GET http://localhost:8000/api/graph/subjects/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Админка

Все модели зарегистрированы в Django админке с настройками:

- **SubjectAdmin**: отображение названия, поиск по названию
- **ConceptAdmin**: отображение названия, предмета и статуса, фильтры по предмету и статусу
- **NodeAdmin**: отображение названия, типа, предмета, концепта и проверяемости, фильтры по типу, предмету, концепту
- **NodeRelationAdmin**: отображение родительского и дочернего узлов, фильтры по предметам узлов

## Тестирование

Приложение покрыто тестами для всех компонентов:

- **GraphModelsTest**: тесты моделей и их методов
- **GraphSerializersTest**: тесты сериализаторов
- **GraphAPITest**: тесты API эндпоинтов, включая фильтрацию и поиск
- **GraphAdminTest**: тесты админки

Запуск тестов:
```bash
# Через Docker Compose
docker-compose exec web python manage.py test graph

# Локально
python manage.py test graph
```

## Зависимости

- `django-filter==24.1` - для фильтрации в API
- `djangorestframework` - для API
- `djangorestframework-simplejwt` - для JWT аутентификации

## Структура файлов

```
graph/
├── __init__.py
├── admin.py          # Регистрация моделей в админке
├── apps.py           # Конфигурация приложения
├── models.py         # Модели данных
├── serializers.py    # Сериализаторы для API
├── tests.py          # Тесты
├── urls.py           # URL-маршруты
├── views.py          # ViewSets для API
├── migrations/       # Миграции базы данных
└── README.md         # Этот файл
```

## Разработка

При разработке новых функций рекомендуется:

1. Создавать тесты для новых моделей и методов
2. Добавлять фильтрацию в ViewSets при необходимости
3. Обновлять сериализаторы при изменении моделей
4. Регистрировать новые модели в админке
5. Обновлять документацию API

## Лицензия

MIT License
