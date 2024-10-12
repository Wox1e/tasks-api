# tasks-api


RESTful API сервис, созданный для управления пользователями и их записями. 

Использует:
- Redis кеширование запросов
- Логгирование в брокер сообщений (RabbitMQ)
- PostgreSQL для храние данных

Установка
Для запуска приложения и вспомогательных сервисов необходимо:
1. Скачать файлы репозитория
2. Создать файл с переменными окружения .env в папке с проектом
3. Скопировать значения по умолчанию (или установить собственные):

REQUESTS_PER_MINUTE_LIMIT = 100

SECRET_KEY = "h(F1k)6ur~{xSVp>'MwF970f0g!Ymapw"

DB_URI = "postgresql://postgres_user:postgres_password@postgres:5432/postgres_db"

BROKER_URI = "logs-rabbitmq-container"

REDIS_HOST = "redis"

REDIS_PORT = 6379

CACHE_TTL = 3



4. Выполнить команду "docker compose -f "docker-compose.yaml" up -d --build " в папке с проектом 
