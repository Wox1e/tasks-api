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


API эндпоинты:
1) /register
   Метод: POST

   Регистрирует нового пользователя

   Обязательные поля: "username":*string*, "password":*string*

   Структура ответа: {"status":true} - успешное выполнение запроса, {"status":false} - ошибка в выполнении запроса

2) /login
   Метод: POST

   Аутентификация пользователя и выдача JWT-токена

   Обязательные поля: "username":*string*, "password":*string*
   
   Необязательные поля: "cookie":*bool* (при значении true API запишет токен в cookie)

   Структура ответа: {"status":false} - ошибка в выполнении запроса, {"status":true, "auth":false} - неверные данные для входа, {"status":true, "auth":true, "token":*token*} - успешное выполнение запроса

3) /logout
   Метод: POST

   Инвалидизация JWT-токена пользователя.
   
   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie]

   Структура ответа: {"status":true} - успешно, {"status":false} - ошибка при выполнении запроса/неверный токен

4) /tasks
   Метод: POST

   Создание новой записи

   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie],"description":*string*

   Структура ответа: {"status":false} - ошибка при выполнении запроса, {"status":true,"auth":true,"added":true} - успешно добавлена запись, {"status":false,"Error":"Bad token or missing token"} - неверный токен

5) /tasks
   Метод: GET

   Получение списка всех записей текущего пользователя.

   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie]

   Структура ответа: {"status":false} - ошибка при выполнении запроса, {*список записей*} - успешное выполнение запроса, {"status":false,"Error":"Bad token or missing token"} - неверный токен

6) /tasks/{task_id}
   
   Метод: GET

   Получение детали конкретной записи по её идентификатору

   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie]

   Структура ответа: {"status":false} - ошибка при выполнении запроса, {*запись*} - успешное выполнение запроса, {"status":false,"Error":"Bad token or missing token"} - неверный токен
   
7) /tasks/{task_id}

   Метод: PUT

   Обновление данных конкретной записи

   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie],"description":*string*

   Структура ответа: {"status":false} - ошибка при выполнении запроса, {"status":true,"auth":true,"updated":true} - успешно обновлена запись, {"status":false,"Error":"Bad token or missing token"} - неверный токен

8) /tasks/{task_id}

   Метод: DELETE

   Удаление конкретной записи

   Обязательные поля: "token":*string* [необязателен, при наличии токена в cookie]

   Структура ответа: {"status":false} - ошибка при выполнении запроса, {"status":true,"auth":true,"deleted":true} - успешно удалена запись, {"status":false,"Error":"Bad token or missing token"} - неверный токен
