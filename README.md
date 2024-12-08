# Readme

## О проекте

Сервис "Электронная очередь при реализации щебня" предназначен для автоматизации процессов подачи заявок, отгрузки и контроля транспортировки щебня на базе АктЗФ. Проект включает разработку серверной части и интеграцию с внешними системами для упрощения взаимодействия с клиентами и партнёрами.

## Стек технологий

- **Backend**: Python (FastAPI, SQLAlchemy)
- **База данных**: PostgreSQL, MySQL
- **Инструменты**: Docker, Redis, Celery
- **Визуализация**: Figma, Canva
- **Аутентификация**: JSON Web Token (JWT)

## Внешние интеграции

- **ERP**: SAP, Qollab
- **Система взвешивания**: MESБ, Автовесовая(Mettler Toledo)
- **Платежные системы**: KaspiPay
- **Пропускная система**: Вездеход

## Инструкция по установке

### Локальная установка

1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Для Windows: .venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` и добавьте переменные окружения (см. таблицу ниже).

5. Запустите приложение:
   ```bash
   uvicorn app.main:app --reload
   ```

### Установка в Docker

1. Клонируйте репозиторий:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Убедитесь, что у вас установлен Docker и Docker Compose.

3. Создайте файл `.env` и добавьте переменные окружения (см. таблицу ниже).

4. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

5. Приложение будет доступно по адресу: `http://localhost:8000`

## Основные команды

- Запуск приложения:
  ```bash
  uvicorn app.main:app --reload
  ```
- Тестирование:
  ```bash
  pytest
  ```
- Статический анализ кода:
  ```bash
  ruff check
  ```
- Форматирование кода:
  ```bash
  ruff format
  ```

## Таблица переменных окружения

| Переменная                  | Описание                                    | Пример значения              |
|-----------------------------|---------------------------------------------|------------------------------|
| `APP_DATABASE`              | Тип базы данных                            | `postgresql`                 |
| `MYSQL_CONNECTION`          | Строка подключения к MySQL                 | `mysql+aiomysql`             |
| `MYSQL_DB_HOST`             | Хост MySQL                                 | `localhost`                  |
| `MYSQL_DB_PORT`             | Порт MySQL                                 | `3306`                       |
| `MYSQL_DB_USER`             | Пользователь MySQL                         | `root`                       |
| `MYSQL_DB_PASSWORD`         | Пароль MySQL                               | `password`                   |
| `MYSQL_DB_NAME`             | Имя базы данных MySQL                      | `queue_test`                 |
| `PG_CONNECTION`             | Строка подключения к PostgreSQL            | `postgresql+asyncpg`         |
| `PG_DB_HOST`                | Хост PostgreSQL                            | `localhost`                  |
| `PG_DB_PORT`                | Порт PostgreSQL                            | `5432`                       |
| `PG_DB_USER`                | Пользователь PostgreSQL                    | `postgres`                   |
| `PG_DB_PASSWORD`            | Пароль PostgreSQL                          | `root`                       |
| `PG_DB_NAME`                | Имя базы данных PostgreSQL                 | `queue_test`                 |
| `DB_POOL_SIZE`              | Размер пула соединений                     | `100`                        |
| `DB_MAX_OVERFLOW`           | Максимальное число дополнительных соединений | `50`                       |
| `DB_POOL_TIMEOUT`           | Тайм-аут ожидания соединения               | `300`                        |
| `DB_POOL_RECYCLE`           | Время жизни соединения                     | `25000`                      |
| `SECRET_KEY`                | Секретный ключ для JWT                     | `your_secret_key`            |
| `ALGORITHM`                 | Алгоритм шифрования JWT                    | `HS256`                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена доступа (в минутах)    | `240`                        |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Время жизни токена обновления (в днях)     | `7`                          |
| `APP_STATUS`                | Статус приложения                          | `DEVELOPMENT`                |
