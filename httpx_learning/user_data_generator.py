import names
from random import randint


def generate_user_data():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    middle_name = names.get_first_name()

    return {
        "firstName": first_name,
        "lastName": last_name,
        "email": f"{first_name.lower()}{last_name.lower()}@example.com",
        "phoneNumber": f"+{randint(1000000000, 9999999999)}",
        "middleName": middle_name,
    }