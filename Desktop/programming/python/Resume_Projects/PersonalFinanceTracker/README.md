# Personal Finance Tracker - Трекер личных финансов

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?style=for-the-badge&logo=docker)

Современное асинхронное приложение для управления личными финансами, построенное на FastAPI и PostgreSQL. Отслеживайте расходы, управляйте бюджетами, ставьте финансовые цели и получайте аналитику о ваших финансовых привычках.

## 📋 Оглавление

- [🚀 Возможности](#-возможности)
- [🛠 Технологический стек](#-технологический-стек)
- [📋 Требования](#-требования)
- [🏃‍♂️ Быстрый старт](#️-быстрый-старт)
- [📁 Структура проекта](#-структура-проекта)
- [🔧 Конфигурация](#-конфигурация)
- [🗄️ База данных](#️-база-данных)
- [📚 Документация API](#-документация-api)
- [🧪 Тестирование](#-тестирование)
- [🐳 Команды Docker](#-команды-docker)
- [🔍 Мониторинг и отладка](#-мониторинг-и-отладка)
- [🤝 Участие в разработке](#-участие-в-разработке)
- [📊 Модели данных](#-модели-данных)
- [🔒 Безопасность](#-безопасность)
- [🚀 Развертывание](#-развертывание)
- [📈 ML-возможности](#-ml-возможности)
- [📄 Лицензия](#-лицензия)
- [🆘 Решение проблем](#-решение-проблем)

## 🚀 Возможности

### Основные функции
- **💰 Учет расходов** - Записывайте и категоризируйте ваши транзакции
- **📊 Управление бюджетами** - Устанавливайте месячные бюджеты и отслеживайте расходы
- **🎯 Финансовые цели** - Откладывайте на конкретные цели с отслеживанием прогресса
- **🔄 Периодические транзакции** - Автоматизируйте регулярные доходы и расходы
- **🏦 Поддержка нескольких счетов** - Управляйте несколькими банковскими счетами
- **💱 Поддержка валют** - Работа с несколькими валютами с реальными курсами

### Дополнительные возможности
- **📈 Аналитика и отчеты** - Визуализация ваших финансовых данных
- **🔐 Безопасная аутентификация** - JWT-аутентификация пользователей
- **🤖 AI-аналитика** - Автоматическая категоризация расходов на основе ML
- **📱 REST API** - Полнофункциональное API для интеграции
- **📊 Визуализация данных** - Графики и диаграммы для анализа финансов

## 🛠 Технологический стек

### Бэкенд
- **FastAPI** - современный, быстрый веб-фреймворк для Python
- **Python 3.11** - последняя стабильная версия Python
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **AsyncPG** - асинхронный драйвер для PostgreSQL
- **Alembic** - система миграций базы данных

### База данных и кэширование
- **PostgreSQL 15** - основная реляционная база данных
- **Redis** - кэширование и управление сессиями

### Аутентификация и безопасность
- **JWT** - JSON Web Tokens для аутентификации
- **bcrypt** - хеширование паролей
- **Pydantic** - валидация данных и настройки

### Аналитика и ML
- **scikit-learn** - машинное обучение для категоризации
- **pandas & numpy** - обработка и анализ данных
- **matplotlib, seaborn, plotly** - визуализация данных

### Документы и отчеты
- **openpyxl** - работа с Excel файлами
- **python-docx** - генерация Word документов
- **reportlab** - создание PDF отчетов

### Контейнеризация
- **Docker** - контейнеризация приложения
- **Docker Compose** - оркестрация контейнеров

## 📋 Требования

### Для продакшн-развертывания
- Docker 20.10+
- Docker Compose 2.0+

### Для локальной разработки
- Python 3.11 или новее
- PostgreSQL 14+
- Redis (опционально)

## 🏃‍♂️ Быстрый старт

### Способ 1: Использование Docker (рекомендуется)

1. **Клонируйте репозиторий**
   ```bash
   git clone <URL-репозитория>
   cd PersonalFinanceTracker
   ```

2. **Настройте переменные окружения**
   ```bash
   # Скопируйте файл с примерами переменных
   cp .env.example .env
   
   # Отредактируйте .env файл под вашу конфигурацию
   nano .env  # или используйте любой текстовый редактор
   ```

3. **Соберите и запустите приложение**
   ```bash
   # Сборка и запуск всех сервисов
   docker-compose up --build
   
   # Или для запуска в фоновом режиме
   docker-compose up -d --build
   ```

4. **Проверьте работу приложения**
   - Основное приложение: http://localhost:8000
   - Автоматическая документация API: http://localhost:8000/docs
   - Альтернативная документация: http://localhost:8000/redoc
   - База данных PostgreSQL: localhost:5432

### Способ 2: Локальная разработка

1. **Создайте виртуальное окружение**
   ```bash
   python -m venv venv
   
   # Активация для Linux/MacOS
   source venv/bin/activate
   
   # Активация для Windows
   venv\Scripts\activate
   ```

2. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте базу данных PostgreSQL**
   ```bash
   # Создайте базу данных (если используется локальный PostgreSQL)
   createdb finance_tracker
   
   # Или настройте подключение к существующей БД в .env файле
   ```

4. **Примените миграции**
   ```bash
   # Если используете Alembic
   alembic upgrade head
   
   # Или запустите кастомные миграции
   python add_remaining_amount_migration.py
   python update_remaining_amount.py
   ```

5. **Запустите приложение**
   ```bash
   python run.py
   ```

## 📁 Структура проекта

```
PersonalFinanceTracker/
├── src/                           # Исходный код приложения
│   ├── models/                   # Модели базы данных
│   │   ├── user.py              # Модель пользователя
│   │   ├── transaction.py       # Модель транзакций
│   │   ├── budget.py            # Модель бюджетов
│   │   ├── goal.py              # Модель финансовых целей
│   │   ├── account.py           # Модель банковских счетов
│   │   ├── category.py          # Модель категорий
│   │   ├── currency.py          # Модель валют
│   │   ├── tag.py               # Модель тегов
│   │   ├── banking.py           # Модель банковских операций
│   │   └── recurring_transaction.py # Модель периодических транзакций
│   ├── schemas/                 # Pydantic схемы для валидации
│   │   ├── user.py              # Схемы пользователя
│   │   ├── transaction.py       # Схемы транзакций
│   │   └── ...                  # Другие схемы
│   ├── core/                    # Основная функциональность
│   │   ├── security.py          # Безопасность и JWT
│   │   └── config.py            # Конфигурация приложения
│   ├── auth.py                  # Маршруты аутентификации
│   ├── database.py              # Подключение к базе данных
│   └── main.py                  # Основное приложение FastAPI
├── migrations/                  # Миграции базы данных (Alembic)
├── tests/                      # Тесты
├── docker-compose.yml          # Docker Compose конфигурация
├── Dockerfile                  # Docker образ приложения
├── requirements.txt            # Зависимости Python
├── run.py                      # Скрипт запуска приложения
├── add_remaining_amount_migration.py  # Кастомные миграции
├── update_remaining_amount.py         # Кастомные миграции
├── .env                        # Переменные окружения (не в репозитории)
├── .env.example                # Пример переменных окружения
├── .gitignore                  # Игнорируемые файлы Git
└── README.md                   # Документация
```

## 🔧 Конфигурация

### Файл .env

Создайте файл `.env` в корне проекта со следующими переменными:

```env
# ===========================================
# НАСТРОЙКИ БАЗЫ ДАННЫХ
# ===========================================
DB_HOST=localhost              # Хост PostgreSQL
DB_PORT=5432                   # Порт PostgreSQL
DB_USER=postgres               # Имя пользователя БД
DB_PASS=postgres               # Пароль пользователя БД
DB_NAME=finance_tracker        # Название базы данных

# ===========================================
# НАСТРОЙКИ БЕЗОПАСНОСТИ
# ===========================================
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256                # Алгоритм шифрования JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Время жизни access token

# ===========================================
# НАСТРОЙКИ ПРИЛОЖЕНИЯ
# ===========================================
HOST=0.0.0.0                   # Хост для запуска приложения
PORT=8000                      # Порт для запуска приложения
RELOAD=true                    # Автоперезагрузка при изменениях (только для разработки)

# ===========================================
# ВНЕШНИЕ СЕРВИСЫ (опционально)
# ===========================================
# REDIS_URL=redis://redis:6379  # URL для Redis
# EXCHANGE_RATE_API_KEY=your-api-key # API ключ для курсов валют
# EMAIL_HOST=smtp.gmail.com     # SMTP сервер для отправки email
# EMAIL_PORT=587                # SMTP порт
# EMAIL_USER=your-email@gmail.com
# EMAIL_PASS=your-app-password
```

### Важные замечания по конфигурации

1. **Секретный ключ (SECRET_KEY)**:
   - Никогда не используйте значение по умолчанию в продакшн
   - Сгенерируйте надежный ключ: `openssl rand -hex 32`
   - Храните секретные ключи в безопасном месте

2. **Настройки базы данных**:
   - Для продакшн используйте отдельного пользователя БД (не postgres)
   - Используйте сложные пароли
   - Рассмотрите использование SSL соединения

3. **Переменные для разных окружений**:
   - Создайте отдельные .env файлы для development, staging, production
   - Используйте разные базы данных для каждого окружения

## 🗄️ База данных

### Основные сущности

1. **Пользователи (Users)** - Учетные записи пользователей
2. **Счета (Accounts)** - Банковские счета и cash
3. **Транзакции (Transactions)** - Доходы и расходы
4. **Категории (Categories)** - Категории транзакций
5. **Бюджеты (Budgets)** - Месячные лимиты расходов
6. **Цели (Goals)** - Финансовые цели для накоплений
7. **Периодические транзакции (Recurring Transactions)** - Автоматические операции

### Миграции

#### Кастомные миграции
Приложение включает специальные скрипты миграций:

```bash
# Применить кастомные миграции
python add_remaining_amount_migration.py
python update_remaining_amount.py
```

#### Alembic миграции (если настроены)
```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1
```

### Подключение к базе данных

Пример конфигурации подключения в `src/database.py`:

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Формирование URL для подключения к PostgreSQL
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, echo=True)  # echo=True для логирования SQL в разработке

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

## 📚 Документация API

### Автоматическая документация

FastAPI автоматически генерирует документацию:

- **Swagger UI**: http://localhost:8000/docs - интерактивная документация с возможностью тестирования API
- **ReDoc**: http://localhost:8000/redoc - альтернативная документация

### Основные эндпоинты API

#### Аутентификация
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "Иван Иванов"
}
```

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com", 
  "password": "securepassword"
}
```

#### Транзакции
```http
GET /transactions/
Authorization: Bearer <jwt-token>

POST /transactions/
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "amount": 1500.50,
  "description": "Покупка продуктов",
  "category_id": 1,
  "account_id": 1,
  "type": "expense"
}
```

#### Бюджеты
```http
GET /budgets/
Authorization: Bearer <jwt-token>

POST /budgets/
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "category_id": 1,
  "amount": 10000.00,
  "month": "2024-01",
  "currency": "RUB"
}
```

#### Цели
```http
GET /goals/
Authorization: Bearer <jwt-token>

POST /goals/
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "name": "Новый ноутбук",
  "target_amount": 150000.00,
  "current_amount": 50000.00,
  "deadline": "2024-12-31"
}
```

### Пример использования с curl

```bash
# Регистрация пользователя
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'

# Вход и получение токена
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'

# Использование токена для доступа к API
curl -X GET "http://localhost:8000/transactions/" \
     -H "Authorization: Bearer <your-jwt-token>"
```

## 🧪 Тестирование

### Запуск тестов

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного тестового файла
pytest tests/test_auth.py

# Запуск тестов с покрытием
pytest --cov=src tests/

# В Docker контейнере
docker-compose exec api pytest
```

### Структура тестов

```
tests/
├── conftest.py           # Фикстуры pytest
├── test_auth.py          # Тесты аутентификации
├── test_transactions.py  # Тесты транзакций
├── test_budgets.py       # Тесты бюджетов
├── test_goals.py         # Тесты целей
└── test_models.py        # Тесты моделей
```

### Пример теста

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_transaction():
    # Аутентификация
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    
    # Создание транзакции
    response = client.post(
        "/transactions/",
        json={
            "amount": 1000.0,
            "description": "Test transaction",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["amount"] == 1000.0
```

## 🐳 Команды Docker

### Основные команды

```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Просмотр логов
docker-compose logs -f api      # Логи приложения
docker-compose logs -f db       # Логи базы данных

# Остановка контейнеров
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Пересборка конкретного сервиса
docker-compose build api

# Проверка статуса контейнеров
docker-compose ps
```

### Команды для разработки

```bash
# Запуск команд внутри контейнера
docker-compose exec api bash           # Открыть shell в контейнере
docker-compose exec api python         # Запустить Python
docker-compose exec api pytest         # Запустить тесты
docker-compose exec api alembic upgrade head  # Применить миграции

# Доступ к базе данных
docker-compose exec db psql -U postgres -d finance_tracker

# Просмотр логов в реальном времени
docker-compose logs -f --tail=100 api
```

### Управление образами

```bash
# Очистка неиспользуемых образов
docker system prune

# Просмотр используемых образов
docker images

# Удаление конкретного образа
docker rmi <image_id>
```

## 🔍 Мониторинг и отладка

### Доступ к базе данных

```bash
# Подключение к PostgreSQL через Docker
docker-compose exec db psql -U postgres -d finance_tracker

# Полезные команды PostgreSQL
\dt                         # Список таблиц
\d+ table_name              # Структура таблицы
SELECT * FROM users;        # Просмотр данных
\q                          # Выход
```

### Отладка приложения

```bash
# Запуск с дебаггером (если настроено)
docker-compose exec api python -m debugpy --listen 0.0.0.0:5678 --wait-for-client run.py

# Просмотр переменных окружения в контейнере
docker-compose exec api env

# Проверка сетевых подключений
docker-compose exec api ping db
```

### Логирование

Приложение использует стандартное логирование Python. Логи можно найти:

```bash
# Просмотр логов приложения
docker-compose logs api

# Просмотр логов с фильтрацией
docker-compose logs api | grep "ERROR"

# Просмотр логов базы данных
docker-compose logs db
```

## 🤝 Участие в разработке

### Процесс разработки

1. **Форк репозитория**
   ```bash
   # Создайте форк на GitHub
   # Затем клонируйте ваш форк
   git clone https://github.com/your-username/PersonalFinanceTracker.git
   cd PersonalFinanceTracker
   ```

2. **Создайте ветку для функции**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Внесите изменения и commit**
   ```bash
   git add .
   git commit -m "Добавлена новая функция: amazing-feature"
   ```

4. **Push в ваш форк**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Создайте Pull Request**

### Стандарты кода

1. **Стиль кода** - Следуем PEP 8
   ```bash
   # Автоформатирование с black
   black src/ tests/
   
   # Проверка стиля с flake8
   flake8 src/ tests/
   ```

2. **Типизация** - Используем type hints
   ```python
   def get_user(user_id: int) -> User:
       return session.get(User, user_id)
   ```

3. **Документация** - Документируем все функции и классы
   ```python
   def calculate_total_expenses(user_id: int, month: str) -> float:
       """
       Рассчитывает общие расходы пользователя за указанный месяц.
       
       Args:
           user_id: ID пользователя
           month: Месяц в формате 'YYYY-MM'
           
       Returns:
           Сумма расходов за месяц
       """
       # implementation
   ```

4. **Тестирование** - Пишем тесты для новой функциональности

### Структура коммитов

```
feat: добавлена новая функция бюджетирования
fix: исправлена ошибка в расчете остатка
docs: обновлена документация API
style: форматирование кода black
refactor: рефакторинг модуля транзакций
test: добавлены тесты для целей
```

## 📊 Модели данных

### Основные отношения

```
User (1) ↔ (N) Account
User (1) ↔ (N) Transaction  
User (1) ↔ (N) Budget
User (1) ↔ (N) Goal
Transaction (N) ↔ (1) Category
Transaction (N) ↔ (1) Account
Budget (N) ↔ (1) Category
Goal (1) ↔ (1) Account
```

### Описание основных моделей

#### User (Пользователь)
```python
class User(Base):
    id: int
    email: str
    hashed_password: str
    full_name: str
    is_active: bool
    created_at: datetime
```
- Хранит информацию о пользователях
- Связь с транзакциями, счетами, бюджетами и целями

#### Transaction (Транзакция)
```python
class Transaction(Base):
    id: int
    amount: float
    description: str
    type: str  # 'income' или 'expense'
    date: datetime
    user_id: int
    category_id: int
    account_id: int
```
- Основная сущность для учета доходов и расходов
- Связана с категорией и счетом

#### Budget (Бюджет)
```python
class Budget(Base):
    id: int
    amount: float
    month: str  # 'YYYY-MM'
    user_id: int
    category_id: int
    currency: str
```
- Месячные лимиты по категориям
- Используется для контроля расходов

## 🔒 Безопасность

### Аутентификация

- **JWT токены** - для stateless аутентификации
- **bcrypt** - для хеширования паролей
- **Время жизни токенов** - настраиваемое время expiration

### Защита данных

- **SQL injection** - защита через SQLAlchemy
- **XSS** - автоматическая экранизация в FastAPI
- **CORS** - настраиваемая политика CORS
- **Валидация данных** - через Pydantic схемы

### Рекомендации для продакшн

1. **Секретные ключи**
   ```bash
   # Генерация надежного секретного ключа
   openssl rand -hex 32
   ```

2. **HTTPS** - Всегда используйте HTTPS в продакшн
3. **CORS политики** - Настройте разрешенные домены
4. **Лимиты запросов** - Реализуйте rate limiting
5. **Аудит безопасности** - Регулярно проверяйте зависимости

## 🚀 Развертывание

### Продакшн настройки

1. **Обновите .env файл**
   ```env
   RELOAD=false
   HOST=0.0.0.0
   SECRET_KEY=your-generated-production-secret
   ```

2. **Docker Compose для продакшн**
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   services:
     api:
       build: .
       environment:
         - RELOAD=false
       restart: always
       
     db:
       image: postgres:15
       restart: always
       volumes:
         - postgres_data:/var/lib/postgresql/data
   ```

3. **Запуск в продакшн**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Рекомендации для продакшн

1. **Обратный прокси** - Настройте nginx или Traefik
2. **SSL сертификаты** - Используйте Let's Encrypt
3. **Мониторинг** - Настройте логирование и мониторинг
4. **Бэкапы** - Регулярно бэкапите базу данных
5. **Обновления** - Регулярно обновляйте зависимости

## 📈 ML-возможности

### Автоматическая категоризация

```python
# Пример использования ML для категоризации
def predict_category(description: str) -> int:
    """
    Автоматически определяет категорию транзакции по описанию
    используя предобученную ML модель
    """
    # implementation with scikit-learn
    return predicted_category_id
```

### Анализ паттернов расходов

- Выявление аномальных трат
- Прогнозирование будущих расходов
- Рекомендации по оптимизации бюджетов

### Обучение моделей

```bash
# Скрипт для обучения ML моделей
python scripts/train_models.py
```

## 📄 Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для деталей.

## 🆘 Решение проблем

### Частые проблемы

1. **Ошибка подключения к базе данных**
   ```bash
   # Проверьте, что PostgreSQL запущен
   docker-compose ps
   
   # Проверьте логи базы данных
   docker-compose logs db
   
   # Проверьте правильность переменных окружения
   docker-compose exec api env | grep DB
   ```

2. **Проблемы с миграциями**
   ```bash
   # Принудительно пересоздайте базу данных
   docker-compose down -v
   docker-compose up --build
   
   # Или примените миграции вручную
   docker-compose exec api python add_remaining_amount_migration.py
   ```

3. **Проблемы с зависимостями**
   ```bash
   # Переустановите зависимости
   docker-compose build --no-cache api
   
   # Или локально
   pip install -r requirements.txt --force-reinstall
   ```

4. **Контейнер не запускается**
   ```bash
   # Проверьте логи
   docker-compose logs api
   
   # Проверьте доступность портов
   netstat -tulpn | grep 8000
   
   # Освободите порт если занят
   sudo lsof -ti:8000 | xargs kill -9
   ```

### Получение помощи

1. Проверьте документацию API на `/docs`
2. Изучите логи приложения: `docker-compose logs api`
3. Проверьте логи базы данных: `docker-compose logs db`
4. Создайте issue в репозитории проекта

### Полезные команды для диагностики

```bash
docker-compose ps

docker stats

docker network ls
docker network inspect personalfinancetracker_default

docker system prune -a
```

---

**Personal Finance Tracker** - Возьмите под контроль ваше финансовое будущее! 💰✨

Для вопросов и предложений создавайте issues в репозитории проекта.