# Подключается встроенный модуль json для работы с форматом JSON
import json

# Определяется строка в формате JSON
json_data = '{"name": "ivan", "age": 70, "is_student": true}'

# json.loads преобразует строку JSON в Python-объект (словарь)
# Результат — dict с ключами name, age, is_student
parsed_data = json.loads(json_data)

# Выводится полученный словарь
print(parsed_data)



# Определяется словарь Python
data = {
    "name": "Ivan",
    "age": 59,
    "is_student": False
}

# json.dumps преобразует словарь в строку JSON
# indent=2 — форматированный вывод с отступами
json_string = json.dumps(data, indent=2)

# Выводится строка в формате JSON и её тип (str)
print(json_string, type(json_string))


# Открывается файл json_example.json для чтения
# json.load читает содержимое файла и преобразует в Python-объект
with open("json_example.json", encoding="utf-8") as file:
    data = json.load(file)
    # Выводится объект (обычно dict) и его тип
    print(data, type(data))


# Открывается файл save_data.json для записи (режим "w" — перезапись)
# json.dump записывает Python-объект в файл в формате JSON
# indent=2 — делает структуру читаемой, ensure_ascii=False — сохраняет кириллицу и спецсимволы
with open("save_data.json", mode= "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii= False)