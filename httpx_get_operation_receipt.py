import httpx
import json
import names
from random import randint


def generate_user_data():
    """генерация рандомных входных данных для создания пользователя.\n
    словарь: имя, фамилия, отчество, почта, номер телефона"""
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


with httpx.Client(base_url="http://localhost:8003/api/v1", timeout=10) as client:
    # Создание пользователя
    created_user_response = client.post("/users", json=generate_user_data())
    created_user_response.raise_for_status()

    created_user_response_data = created_user_response.json()
    print(
        f"User created:\n{json.dumps(created_user_response_data, indent=2, ensure_ascii=False)}"
    )

    # Открытие кредитного счета
    open_credit_card_account_body = {"userId": created_user_response_data["user"]["id"]}
    open_credit_card_account_response = client.post(
        "/accounts/open-credit-card-account", json=open_credit_card_account_body
    )
    open_credit_card_account_response.raise_for_status()

    open_credit_card_account_data = open_credit_card_account_response.json()
    print(
        f"Credit card account opened:\n{json.dumps(open_credit_card_account_data, indent=2, ensure_ascii=False)}"
    )

    # Подготовка данных для осуществления покупки
    account_id = open_credit_card_account_data["account"]["id"]
    card_id = open_credit_card_account_data["account"]["cards"][0]["id"]
    make_purchase_operation_body = {
        "status": "IN_PROGRESS",
        "amount": 77.99,
        "category": "taxi",
        "cardId": card_id,
        "accountId": account_id,
    }

    # Произведение покупки
    make_purchase_operation_response = client.post(
        "/operations/make-purchase-operation", json=make_purchase_operation_body
    )
    make_purchase_operation_response.raise_for_status()

    make_purchase_operation_data = make_purchase_operation_response.json()
    print(
        f"Purchase operation data:\n{json.dumps(make_purchase_operation_data, indent=2, ensure_ascii=False)}"
    )

    # Получение чека операции
    operation_id = make_purchase_operation_data["operation"]["id"]
    get_operation_receipt_response = client.get(f"/operations/operation-receipt/{operation_id}")
    get_operation_receipt_response.raise_for_status()
    get_operation_receipt_data = get_operation_receipt_response.json()

    print(
        f"Purchase receipt:\n{json.dumps(get_operation_receipt_data, indent=2, ensure_ascii=False)}"
    )