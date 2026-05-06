# 🎮 Team Spirit - Установка и настройка

## Требования

- **Python**: 3.11 или выше
- **pip**: последняя версия
- **SQLite**: встроенная в Python (по умолчанию)

## Версии зависимостей

| Пакет | Версия |
|-------|--------|
| Django | 5.0.4 |
| djangorestframework | 3.15.1 |
| django-cors-headers | 4.3.1 |
| Pillow | 10.3.0 |

## Пошаговая установка

### 1. Клонирование и переход в директорию

```bash
cd backend
```

### 2. Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

```bash
python manage.py makemigrations core
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите:
- Имя пользователя: `admin`
- Email: `admin@teamspirit.ru`
- Пароль: (ваш пароль)

### 6. Заполнение тестовыми данными (опционально)

```bash
python scripts/seed_data.py
```

### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Сайт будет доступен по адресу: http://127.0.0.1:8000

## Структура проекта

```
backend/
├── team_spirit/           # Основной проект Django
│   ├── __init__.py
│   ├── settings.py        # Настройки проекта
│   ├── urls.py            # Главные URL маршруты
│   └── wsgi.py            # WSGI конфигурация
├── core/                  # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления (страницы)
│   ├── api_views.py       # API представления
│   ├── serializers.py     # Сериализаторы для API
│   ├── admin.py           # Административная панель
│   ├── urls.py            # URL маршруты приложения
│   └── api_urls.py        # URL маршруты API
├── templates/             # HTML шаблоны
│   ├── base.html          # Базовый шаблон
│   └── core/              # Шаблоны приложения
├── static/                # Статические файлы
├── media/                 # Загружаемые файлы
├── scripts/               # Скрипты
│   └── seed_data.py       # Заполнение тестовыми данными
├── manage.py              # Утилита управления Django
└── requirements.txt       # Зависимости Python
```

## Доступные страницы

| URL | Описание |
|-----|----------|
| `/` | Главная страница |
| `/team/` | Страница команды |
| `/news/` | Список новостей |
| `/news/<slug>/` | Детальная страница новости |
| `/matches/` | Расписание матчей |
| `/achievements/` | Достижения |
| `/partners/` | Партнёры |
| `/about/` | О команде |
| `/admin/` | Административная панель |

## REST API

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/disciplines/` | GET | Список дисциплин |
| `/api/players/` | GET | Список игроков |
| `/api/players/<id>/` | GET | Детали игрока |
| `/api/news/` | GET | Список новостей |
| `/api/matches/` | GET | Список матчей |
| `/api/achievements/` | GET | Список достижений |
| `/api/team-info/` | GET | Информация о команде |

### Примеры запросов API

**Получить игроков по дисциплине:**
```
GET /api/players/?discipline=dota2
```

**Получить последние 5 новостей:**
```
GET /api/news/?limit=5
```

**Получить предстоящие матчи:**
```
GET /api/matches/?status=upcoming
```

## Административная панель

После создания суперпользователя перейдите на http://127.0.0.1:8000/admin/

В админке доступно управление:
- Дисциплинами
- Игроками
- Достижениями
- Матчами
- Новостями
- Партнёрами
- Информацией о команде

## Конфигурация для продакшена

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Сбор статических файлов

```bash
python manage.py collectstatic
```

### Gunicorn (Linux)

```bash
pip install gunicorn
gunicorn team_spirit.wsgi:application --bind 0.0.0.0:8000
```

## Возможные проблемы

### Ошибка "No module named 'core'"

Убедитесь, что вы находитесь в директории `backend`:
```bash
cd backend
python manage.py runserver
```

### Ошибка миграций

Удалите файл `db.sqlite3` и папки `migrations` внутри приложений, затем:
```bash
python manage.py makemigrations core
python manage.py migrate
```

### Статические файлы не загружаются

В режиме разработки Django автоматически обслуживает статику. В продакшене настройте nginx или whitenoise.

---

🎮 **Team Spirit** - Вперёд к победе!
