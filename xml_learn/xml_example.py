# Импортируется модуль для работы с XML, сокращённо ET
import xml.etree.ElementTree as ET


# Определяется XML-документ в виде многострочной строки
xml_data = """
<user>
    <id>1</id>
    <first_name>John</first_name>
    <last_name>Doe</last_name>
    <email>jodo@mail.ru</email>
    <address>
        <street>Main street</street>
        <city>New York</city>
        <zip>10001</zip>
    </address>
</user>
"""


# Разбор XML-строки в дерево элементов
# Результат — объект Element, корневой элемент дерева — <user>
root = ET.fromstring(xml_data)

# Метод find ищет первый тег <email> внутри root
# Атрибут text возвращает текст внутри тега: "jodo@mail.ru"
print(root.find("email").text)
