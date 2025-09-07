# Демонстрируется использование синхронного httpx.Client с base_url, создание ресурса (POST),
# извлечение идентификатора из JSON-ответа, чтение ресурса по id (GET) и базовая проверка статуса.

import httpx   # импортируется клиент HTTP с поддержкой connection pooling
import time    # импортируется модуль для генерации уникальной части e-mail

# Открывается контекстный менеджер клиента: соединения переиспользуются, по выходу закрываются.
# Параметр base_url задаёт общий префикс для всех относительных путей.
with httpx.Client(base_url="http://localhost:8003") as client:
    # Готовится тело запроса для создания пользователя.
    # В e-mail подставляется текущее время, чтобы обеспечивалась уникальность.
    create_user_body = {
        "email": f"httpx_user_{time.time()}@example.com",
        "lastName": "user",
        "firstName": "httpx",
        "middleName": "none",
        "phoneNumber": "+48291293",
    }

    # Выполняется POST на endpoint создания пользователя; json= сериализуется в JSON и
    # автоматически устанавливается заголовок Content-Type: application/json.
    create_user_response = client.post("/api/v1/users", json=create_user_body)

    # Выполняется проверка статуса ответа: при кодах 4xx/5xx выбрасывается HTTPStatusError.
    create_user_response.raise_for_status()

    # Выполняется парсинг тела ответа как JSON; ожидается словарь с ключом "user".
    create_user_response_data = create_user_response.json()
    
    
    # Формируется GET-запрос для чтения пользователя по id, извлечённому из предыдущего ответа.
    # ВАЖНО: в текущей строке возникает конфликт кавычек внутри f-строки:
    # f"/api/v1/users/{create_user_response_data["user"]["id"]}"
    # В реальном коде рекомендуется использовать внешние одинарные кавычки или экранирование,
    # чтобы предотвращалась синтаксическая ошибка (SyntaxError).
    get_user_response = client.get(f'/api/v1/users/{create_user_response_data["user"]["id"]}')

    # Выполняется проверка статуса ответа.
    get_user_response.raise_for_status()

    # Выполняется парсинг JSON-ответа сервера по пользователю.
    get_user_response_data = get_user_response.json()
    

    # Выполняется вывод полученных данных пользователя в консоль.
    print(f"Retrieved user: {get_user_response_data}")

# Примечания для практики:
# - В продакшн-коде обычно настраивается timeout= и внедряется повторная отправка (retry) по политикам.
# - Для батчевых сценариев и частых вызовов используется единый Client, как показано выше.
# - Структура JSON-ответов должна уточняться по контракту API (ожидается наличие поля user.id).