# httpx — современная библиотека HTTP для Python (альтернатива requests): поддерживает HTTP/1.1 и HTTP/2,
# синхронный и асинхронный режимы, connection pooling, cookies, заголовки по умолчанию, таймауты и пр.
# Ниже — мини-лекция через примеры: GET/POST, headers/params, загрузка файлов, Client с base_url, обработка ошибок и таймауты.

import httpx  # импортируем синхронный API httpx (есть и асинхронный: httpx.AsyncClient)

# БАЗОВЫЙ GET-запрос. Вызов httpx.get(...) создаёт новый клиент под капотом и сразу делает запрос.
response = httpx.get("https://jsonplaceholder.typicode.com/todos/1")

print(response.status_code)  # статус-код HTTP (200, 404, 500 и т.д.)
print(response.json())       # .json() — попытка распарсить тело ответа как JSON в Python-объекты
print(response.text)         # .text — исходный текст ответа (строка), полезно для не-JSON контента


# БАЗОВЫЙ POST с JSON-телом. Аргумент json= сериализует питоновский dict в JSON и ставит Content-Type: application/json.
data = {
  "userId": 233,
  "title": "new task",
  "completed": False
}
response = httpx.post("https://jsonplaceholder.typicode.com/todos", json=data)
print(f"{response.status_code}\n{response.json()}")  # печатаем код и ответ сервера как JSON


# ДОБАВЛЕНИЕ ЗАГОЛОВКОВ. headers= позволяет передавать, например, токены авторизации (Bearer ...).
headers = {"Authorization": "Bearer Token-Chpoken"}
response = httpx.get("https://httpbin.org/get", headers=headers)

print(f"{response.status_code}\n{response.json()}")  # httpbin вернёт то, что получил, полезно для отладки


# QUERY-ПАРАМЕТРЫ. params= сериализует dict в строку запроса (?key=value).
params = {"userId": 1}
response = httpx.get("https://jsonplaceholder.typicode.com/todos", params=params)

print(response.request.url)                 # .request.url — фактический URL после подстановки params
print(f"{response.status_code}\n{response.json()}")  # сервер вернёт список задач userId=1


# ОТПРАВКА ФАЙЛОВ multipart/form-data. files= принимает словарь: имя поля -> (имя_файла, бинарный_объект_файла).
# В продакшне файл лучше открывать через контекстный менеджер: with open(...) as f: ...
files = {"file": ("example.txt", open("example.txt", "rb"))}
response = httpx.post("https://httpbin.org/post", files=files)

print(f"{response.status_code}\n{response.json()}")  # httpbin покажет полученные файлы/поля


# ЯВНЫЙ КЛИЕНТ. Используем httpx.Client для переиспользования соединений (connection pooling), общих настроек и cookies.
# Это эффективнее, чем каждый раз вызывать httpx.get/post: меньше накладных расходов на TCP/TLS.
with httpx.Client() as client:
    # Повторяем примеры GET/POST уже через постоянный клиент.
    response_1 = client.get("https://jsonplaceholder.typicode.com/todos/1")
    data = {"userId": 233, "title": "new task", "completed": False}
    response_2 = client.post("https://jsonplaceholder.typicode.com/todos", json=data)

print(response_1.json())  # читаем JSON из ответа GET
print(response_2.json())  # читаем JSON из ответа POST


# КЛИЕНТ С ГЛОБАЛЬНЫМИ НАСТРОЙКАМИ: общие headers, base_url и params применяются ко всем запросам клиента.
client = httpx.Client(
    headers={"Authorization": "Bearer Token-Chpoken"},  # общий заголовок авторизации
    base_url="https://jsonplaceholder.typicode.com",    # базовый URL — маршруты можно задавать как относительные
    params={"userId": 1}                                # общий query-параметр добавится ко всем запросам
)
response_1 = client.get("/todos/1")  # получится https://jsonplaceholder.typicode.com/todos/1?userId=1
data = {"userId": 233, "title": "new task", "completed": False}
response_2 = client.post("/todos", json=data)

print(response_1.request.url)  # убеждаемся, что base_url и params применились
print(response_1.json())
print(response_2.request.url)
print(response_2.json())

# ОБРАБОТКА ОШИБОК. raise_for_status() выбросит httpx.HTTPStatusError при статусах 4xx/5xx.
try:
    response = httpx.get("https://jsonplaceholder.typicode.com/todos/invalid_url")
    response.raise_for_status()  # если 404/500, перейдём в except
except httpx.HTTPStatusError as e:
    print(f"ОШИБКА: НЕТ ТАКОЙ ЮРЭЭЛ: {e}")  # в реальном коде логируйте и реагируйте по контексту


# ТАЙМАУТЫ. timeout= (в секундах) контролирует максимальное ожидание (по умолчанию в httpx есть безопасные значения).
# Здесь сервер задерживает ответ на ~5 секунд — первый запрос успевает, второй — нет.
response = httpx.get("https://httpbin.org/delay/5", timeout=10)
print(response)  # успешный ответ (10с > 5с)

try:
    response = httpx.get("https://httpbin.org/delay/5", timeout=2)  # 2с < 5с — будет ReadTimeout
except httpx.ReadTimeout as e:
    print(f"Превышено время ожидания: {e}")  # обрабатываем таймаут: можно повторить запрос/сообщить пользователю

# ИТОГ:
# - Для разовых обращений подходят функции httpx.get/post(...).
# - Для множества запросов — используйте httpx.Client (эффективность и общие настройки).
# - json=, params=, headers= и files= покрывают типовые сценарии API.
# - Обязательно оборачивайте критичные вызовы в try/except и настраивайте таймауты.
# - Для асинхронных приложений есть httpx.AsyncClient с тем же API (await client.get(...)).