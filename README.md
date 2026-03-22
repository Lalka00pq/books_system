# Books System API

Реализация REST API для ведения книг пользователей с поддержкой JWT-авторизации, полного набора CRUD-операций и разделением прав ролей (Admin / User).

## Предметная область
Система представляет собой общий каталог книг и личные списки пользователей (добавление книг в список для чтения с указанием статуса).
База данных представляет собой три таблицы:
- `users` (пользователи)
- `books` (книги)
- `user_books` (связь пользователей и книг)
## Описание таблиц базы данных
### `users`

| Поле | Тип | Описание |
|------|-----|-----------|
| id | SERIAL Not Null | Идентификатор пользователя (генеруется автоматически) | 
| email | VARCHAR(255) Not Null | Email пользователя |
| password | VARCHAR Not Null | Пароль пользователя (хешированный) |
| role | ENUM('USER', 'ADMIN') Not Null | Роль пользователя |
| created_at | TIMESTAMP Not Null | Дата и время создания |
| updated_at | TIMESTAMP Not Null | Дата и время обновления |

### `books`

| Поле | Тип | Описание |
|------|-----|-----------|
| id | SERIAL Not Null | Идентификатор книги (генеруется автоматически) |
| title | VARCHAR(100) Not Null | Название книги |
| author | VARCHAR(100) Not Null | Автор книги |
| genre | VARCHAR(50) | Жанр книги |
| description | TEXT | Описание книги |
| created_at | TIMESTAMP Not Null | Дата и время создания |
| updated_at | TIMESTAMP Not Null | Дата и время обновления |
| isbn | VARCHAR(20) | ISBN книги |
| publisher | VARCHAR(100) | Издательство |
| publication_date | DATE | Дата публикации |

### `user_books`
| Поле | Тип | Описание |
|------|-----|-----------|
| id | SERIAL Not Null | Идентификатор записи (генеруется автоматически) |
| user_id | INTEGER Not Null ForeignKey | Идентификатор пользователя |
| book_id | INTEGER Not Null ForeignKey | Идентификатор книги |
| status | ENUM('PLAN_TO_READ', 'READING', 'READ', 'ABANDONED') Not Null | Статус книги |
| created_at | TIMESTAMP Not Null | Дата и время создания |
| updated_at | TIMESTAMP Not Null | Дата и время обновления |
| added_at | TIMESTAMP Not Null | Дата и время добавления книги в список для чтения |

## Стек технологий
- **Язык**: Python 3.11+
- **Фреймворк**: FastAPI
- **ORM**: SQLAlchemy (Async)
- **База данных**: PostgreSQL 17
- **Миграции**: Alembic
- **Валидация**: Pydantic v2
- **Безопасность**: JWT (python-jose), Bcrypt (passlib)

## Как запустить проект
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Lalka00pq/books_system
   ```
2. Перейдите в папку проекта
   ```bash
   cd books_system
   ```
3. Создайте виртуальное окружение:
   Для MacOS/Linux:
   ```bash
   python3 -m venv .venv
   ```
   Активируем окружение:
   ```bash
   source .venv/bin/activate
   ```
   Устанавливаем зависимости:
   Использование pip:
   ```bash
   pip install -r requirements.txt
   ```
   Использование uv:
   ```bash
   uv sync
   ```
   Для Windows:
   ```bash
   python -m venv .venv
   ```   
   Активируем окружение:
   ```bash
   .venv\Scripts\activate
   ```
   Устанавливаем зависимости:
   Использование pip:
   ```bash
   pip install -r requirements.txt
   ```
   Использование uv:
   ```bash
   uv sync
   ```
4. Настройте `.env` файл.
   Переименуйте файл `.env.example` в `.env`. Укажите в файле данные для подключения к базе данных
5. Примените миграции (Если база данных пустая будут созданы таблицы и данные):
   ```bash
   alembic upgrade head
   ```
6. Запустите сервер:
   ```bash
   uvicorn app.main:app --reload
   ```
   или 
   ```bash
   fastapi run app/main.py --reload
   ```

## Маршруты API
Полная документация: `http://127.0.0.1:8000/docs`

### Авторизация
- `POST /api/v1/auth/login` — Вход по **email** и паролю, получает JWT.
- `POST /api/v1/auth/logout` — Выход.

### Личный список книг (Требуется авторизация)
- `GET /api/v1/books` — Получить свои книги.
- `POST /api/v1/books` — Добавить книгу из каталога в свой список.
- `GET /api/v1/books/{association_id}` — Получить конкретную книгу.
- `PUT /api/v1/books/{association_id}` — Изменить конкретную книгу.
- `DELETE /api/v1/books/{association_id}` — Удалить книгу из списка.


### Глобальный каталог книг
- `GET /api/v1/catalog/show_catalog` — Просмотр всех книг (Требуется авторизация).
- **CRUD операции для админов (роль ADMIN):**
  - `POST /api/v1/catalog/add_to_catalog` Добавить книгу в каталог.
  - `PUT /api/v1/books/catalog/update_catalog/{id}` Обновить книгу в каталоге.
  - `PATCH /api/v1/books/catalog/patch_catalog/{id}` Частично обновить книгу в каталоге.
  - `DELETE /api/v1/books/catalog/delete_from_catalog/{id}` Удалить книгу из каталога.

Примеры запросов:
Для отправки запросов лучше использовать Swagger http://127.0.0.1:8000/docs.
### Авторизация (api/v1/auth/login)
Для пользователя:
```json
{
    "email": "student@example.com",
    "password": "student123"
}
```
Для админа:
```json
{
    "email": "admin@example.com",
    "password": "admin"
}
```
### Работа с книгами в личном списке (api/v1/books)
При добавлении книг в базу данных им присваивается случайный id. Чтобы увидеть какие книги можно добавить, нужно выполнить запрос:
Endpoint: `GET /api/v1/сatalog/show_catalog`
Далее пример на добавление книги:
Ответ (пример):
```json
[
  {
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "isbn": "978-5-17-085350-2",
    "genre": "Classic",
    "description": "A novel about racial injustice in the Deep South.",
    "publisher": "J.B. Lippincott & Co.",
    "publish_date": "1960-07-11",
    "id": "a0a3276b-11c4-49bc-a504-2ef28cd52143", # Данный ID нужно будет указывать при добавлении книги в список
    "created_at": "2026-03-14T17:53:20.149709",
    "updated_at": "2026-03-14T17:53:20.149709"
  },
  {
    "title": "Neuromancer",
    "author": "William Gibson",
    "isbn": "978-5-699-90603-1",
    "genre": "Science Fiction",
    "description": "A novel that coined the term cyberspace.",
    "publisher": "Ace Books",
    "publish_date": "1984-07-01",
    "id": "fd23715f-793c-4eaf-9d98-2fb0e6b4093f",
    "created_at": "2026-03-14T17:53:20.149709",
    "updated_at": "2026-03-14T17:53:20.149709"
  }]
```
Добавление книги:
POST /api/v1/books
```json
{
  "status": "plan_to_read",
  "book_id": "a0a3276b-11c4-49bc-a504-2ef28cd52143" # ID книги из каталога
}
```
Изменение статуса книги:
PUT /api/v1/books/{association_id}
Обязательно указывается association_id - id книги в личном списке. После добавления книги, у пользователя есть возможность увидеть все книги в личном списке. Для этого нужно выполнить запрос:
GET /api/v1/books
Ответ будет, например, такой:
```json
[
  {
    "status": "plan_to_read",
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", # указывать в PUT запросе нужно данный ID
    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "book_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "added_at": "2026-03-15T10:34:15.245Z",
    "book": {
      "title": "string",
      "author": "string",
      "isbn": "string",
      "genre": "string",
      "description": "string",
      "publisher": "string",
      "publish_date": "2026-03-15",
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "created_at": "2026-03-15T10:34:15.245Z",
      "updated_at": "2026-03-15T10:34:15.245Z"
    }
  }
]
```
Указываем association_id и отправляем такой json
```json
{
  "status": "completed"
}
```
Удаление книги из списка:
DELETE /api/v1/books/{association_id} - тот же id, что и в PUT запросе

### Работа с книгами в каталоге (api/v1/catalog)
Получение всех книг в каталоге:
GET /api/v1/catalog/show_catalog

Добавление книги в каталог (доступно только для админов):
POST /api/v1/catalog/add_to_catalog
```json
{
    "title": "Count Zero",
    "author": "William Gibson",
    "isbn": "978-5-699-70603-1",
    "genre": "Science Fiction",
    "description": "Cyberpunk novel",
    "publisher": "Ace Books",
    "publish_date": "1984-07-01"
  }
```
Изменение книги в каталоге (доступно только для админов):
PUT /api/v1/catalog/update_catalog/{id} id - id книги в каталоге (таблица books)
PATCH /api/v1/catalog/patch_catalog/{id}
```json
{
  "title": "test",
  "author": "test",
  "isbn": "",
  "genre": "",
  "description": "",
  "publisher": "",
  "publish_date": "2026-03-15"
}
```
Удаление книги из каталога (доступно только для админов):
DELETE /api/v1/catalog/delete_from_catalog/{id} id - id книги в каталоге (таблица books)

## Структура проекта
```
├── .env - файл с переменными окружения
├── .gitignore - файл игнорирования
├── alembic.ini - конфигурация alembic
├── alembic - alembic миграции
├── app - приложение
│    ├── api - Endpoints
│    ├── core - логика приложения
│    ├── database - база данных
│    ├── models - модели данных
│    ├── schemas - схемы данных для валидации
│    ├── services - сервисы
│    ├── main.py - файл запуска приложения
│    ├── config.py - конфигурация приложения
│    ├── dependencies.py - зависимости
```