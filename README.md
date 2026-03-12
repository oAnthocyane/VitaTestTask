# Diary API - Приложение-ежедневник

REST API для управления записями в ежедневнике, построенное на FastAPI с использованием Clean Architecture.

## Описание

Приложение предоставляет полный CRUD функционал для работы с записями ежедневника:
- Создание, чтение, обновление и удаление записей
- Фильтрация записей по статусу выполнения
- Отметка записей как выполненных
- Автоматическое отслеживание времени создания и обновления

## Технологический стек

- **Python 3.13+**
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy 2.0+** - ORM с async поддержкой
- **PostgreSQL** - база данных
- **Alembic** - миграции БД
- **Pydantic** - валидация данных
- **Granian** - ASGI сервер с hot reload
- **uv** - менеджер пакетов

## Архитектура

Проект следует принципам Clean Architecture с разделением на слои:
- **Models** - SQLAlchemy модели (БД)
- **Schemas** - Pydantic схемы (валидация)
- **Repositories** - доступ к данным
- **Services** - бизнес-логика
- **Use Cases** - оркестрация операций
- **Router** - HTTP endpoints
- **Dependency Injection** - связывание компонентов

## Установка и запуск

### 1. Клонирование и установка зависимостей

```bash
# Установите uv (если еще не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установите зависимости
uv sync
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Настройте переменные окружения в `.env`:

```env
TEST_TASK_APP__DEBUG=true
TEST_TASK_APP__BASE_URL=http://localhost:8080
TEST_TASK_APP__SECRET_KEY=your-secret-key-here
TEST_TASK_APP__CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Database
TEST_TASK_APP__DB__HOST=localhost
TEST_TASK_APP__DB__PORT=5432
TEST_TASK_APP__DB__USER=postgres
TEST_TASK_APP__DB__PASSWORD=your-password
TEST_TASK_APP__DB__NAME=diary_db
TEST_TASK_APP__DB__SCHEME=public
```

### 3. Создание базы данных

```bash
# Создайте базу данных PostgreSQL
createdb diary_db

# Или через psql
psql -U postgres -c "CREATE DATABASE diary_db;"
```

### 4. Применение миграций

```bash
# Создайте и примените миграции
bash make_migrate_and_migrate.sh "Initial migration"
```

### 5. Запуск приложения

```bash
# Запуск с hot reload
bash run.sh

# Или напрямую
uv run python -m test_task.main
```

Приложение будет доступно по адресу: http://localhost:8080

## API Документация

### Интерактивная документация

- **Swagger UI**: http://localhost:8080/docs
- **OpenAPI JSON**: http://localhost:8080/docs.json

### Endpoints

#### 1. Создать запись

```http
POST /api/diary/
Content-Type: application/json

{
  "title": "Купить продукты",
  "content": "Молоко, хлеб, яйца"
}
```

**Ответ (201 Created):**
```json
{
  "title": "Купить продукты",
  "content": "Молоко, хлеб, яйца",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "isCompleted": false,
  "createdAt": "2026-03-13T10:30:00Z",
  "updatedAt": "2026-03-13T10:30:00Z"
}
```

#### 2. Получить список записей

```http
GET /api/diary/
```

**Query параметры:**
- `filter_by` (optional): `completed` | `pending` | не указан (все записи)

**Примеры:**
```http
GET /api/diary/                    # Все записи
GET /api/diary/?filter_by=pending  # Только невыполненные
GET /api/diary/?filter_by=completed # Только выполненные
```

**Ответ (200 OK):**
```json
{
  "items": [
    {
      "title": "Купить продукты",
      "content": "Молоко, хлеб, яйца",
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "isCompleted": false,
      "createdAt": "2026-03-13T10:30:00Z",
      "updatedAt": "2026-03-13T10:30:00Z"
    }
  ],
  "total": 1
}
```

#### 3. Получить запись по ID

```http
GET /api/diary/{entry_id}
```

**Пример:**
```http
GET /api/diary/550e8400-e29b-41d4-a716-446655440000
```

**Ответ (200 OK):**
```json
{
  "title": "Купить продукты",
  "content": "Молоко, хлеб, яйца",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "isCompleted": false,
  "createdAt": "2026-03-13T10:30:00Z",
  "updatedAt": "2026-03-13T10:30:00Z"
}
```

#### 4. Обновить запись

```http
PUT /api/diary/{entry_id}
Content-Type: application/json

{
  "title": "Купить продукты (обновлено)",
  "content": "Молоко, хлеб, яйца, масло"
}
```

**Ответ (200 OK):**
```json
{
  "title": "Купить продукты (обновлено)",
  "content": "Молоко, хлеб, яйца, масло",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "isCompleted": false,
  "createdAt": "2026-03-13T10:30:00Z",
  "updatedAt": "2026-03-13T11:00:00Z"
}
```

#### 5. Отметить запись выполненной

```http
PATCH /api/diary/{entry_id}/complete
```

**Ответ (200 OK):**
```json
{
  "title": "Купить продукты",
  "content": "Молоко, хлеб, яйца",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "isCompleted": true,
  "createdAt": "2026-03-13T10:30:00Z",
  "updatedAt": "2026-03-13T12:00:00Z"
}
```

#### 6. Удалить запись

```http
DELETE /api/diary/{entry_id}
```

**Ответ (200 OK):**
```json
{
  "status": "ok"
}
```

## Обработка ошибок

API возвращает структурированные ошибки в следующем формате:

### 404 Not Found - Запись не найдена

```json
{
  "detail": "Model DiaryEntry with id=550e8400-e29b-41d4-a716-446655440000 not found",
  "error_code": "MODEL_NOT_FOUND",
  "error_type": "ModelNotFoundException",
  "extras": {
    "model": "DiaryEntry",
    "id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

### 422 Unprocessable Entity - Ошибка валидации

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {
        "min_length": 1
      }
    }
  ]
}
```

### 500 Internal Server Error - Внутренняя ошибка сервера

```json
{
  "detail": "Internal server error"
}
```

## Структура проекта

```
.
├── test_task/                      # Основной пакет приложения
│   ├── apps/                       # Бизнес-модули
│   │   └── diary/                  # Модуль ежедневника
│   │       ├── models.py           # SQLAlchemy модели
│   │       ├── schemas.py          # Pydantic схемы
│   │       ├── repositories/       # Репозитории (доступ к БД)
│   │       ├── services/           # Бизнес-логика
│   │       ├── use_cases/          # Use cases
│   │       ├── router.py           # HTTP endpoints
│   │       └── depends.py          # Dependency injection
│   ├── core/                       # Общая инфраструктура
│   │   ├── db.py                   # Настройка БД
│   │   ├── models.py               # Базовые модели
│   │   ├── schemas.py              # Базовые схемы
│   │   ├── repositories/           # Базовый репозиторий
│   │   └── utils/                  # Утилиты
│   ├── main.py                     # Точка входа
│   ├── bootstrap.py                # Фабрика приложения
│   ├── settings.py                 # Конфигурация
│   ├── router.py                   # Агрегация роутов
│   ├── middleware.py               # Middleware
│   └── exceptions.py               # Обработчики исключений
├── migrations/                     # Alembic миграции
├── pyproject.toml                  # Зависимости
├── .env                            # Переменные окружения
├── run.sh                          # Скрипт запуска
└── README.md                       # Документация
```

## Модель данных

### DiaryEntry

| Поле | Тип | Описание |
|------|-----|----------|
| id | UUID | Уникальный идентификатор (генерируется автоматически) |
| title | String(255) | Заголовок записи |
| content | Text | Содержание записи |
| is_completed | Boolean | Статус выполнения (по умолчанию false) |
| created_at | DateTime | Время создания (UTC, автоматически) |
| updated_at | DateTime | Время последнего обновления (UTC, автоматически) |

## Разработка

### Создание миграций

```bash
# Автоматическая генерация миграции
bash make_migrate_and_migrate.sh "Description of changes"

# Или вручную
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Откат миграций

```bash
# Откатить последнюю миграцию
alembic downgrade -1

# Откатить все миграции
alembic downgrade base
```

### Проверка кода

```bash
# Запуск линтера (если настроен)
uv run ruff check .

# Форматирование кода
uv run ruff format .
```

## Примеры использования

### cURL

```bash
# Создать запись
curl -X POST http://localhost:8080/api/diary/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Задача", "content": "Описание задачи"}'

# Получить все записи
curl http://localhost:8080/api/diary/

# Получить запись по ID
curl http://localhost:8080/api/diary/550e8400-e29b-41d4-a716-446655440000

# Обновить запись
curl -X PUT http://localhost:8080/api/diary/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{"title": "Обновленная задача", "content": "Новое описание"}'

# Отметить выполненной
curl -X PATCH http://localhost:8080/api/diary/550e8400-e29b-41d4-a716-446655440000/complete

# Удалить запись
curl -X DELETE http://localhost:8080/api/diary/550e8400-e29b-41d4-a716-446655440000
```

### Python (httpx)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8080") as client:
        # Создать запись
        response = await client.post(
            "/api/diary/",
            json={"title": "Задача", "content": "Описание"}
        )
        entry = response.json()
        entry_id = entry["id"]
        
        # Получить запись
        response = await client.get(f"/api/diary/{entry_id}")
        print(response.json())
        
        # Отметить выполненной
        response = await client.patch(f"/api/diary/{entry_id}/complete")
        print(response.json())

asyncio.run(main())
```