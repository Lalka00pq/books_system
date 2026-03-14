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
   python3 -m venv venv
   ```
   Активируем окружение:
   ```bash
   source venv/bin/activate
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
   python -m venv venv
   ```   
   Активируем окружение:
   ```bash
   venv\Scripts\activate
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
5. Примените миграции:
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