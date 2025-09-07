import httpx
import json
from user_data_generator import generate_user_data


with httpx.Client(base_url="http://localhost:8003/api/v1", timeout=10) as client:
    # Создание пользователя
    created_user_response = client.post("/users", json=generate_user_data())
    created_user_response.raise_for_status()
    created_user_response_data = created_user_response.json()

    print(
        f"User created:\n{json.dumps(created_user_response_data, indent=2, ensure_ascii=False)}"
    )

    # Открытие дебетового счета
    open_debit_card_account_body = {"userId": created_user_response_data["user"]["id"]}
    open_debit_card_account_response = client.post(
        "/accounts/open-debit-card-account", json=open_debit_card_account_body
    )
    open_debit_card_account_response.raise_for_status()
    open_debit_card_account_data = open_debit_card_account_response.json()

    print(
        f"Debit card account opened:\n{json.dumps(open_debit_card_account_data, indent=2, ensure_ascii=False)}"
    )

    account_id = open_debit_card_account_data["account"]["id"]
    card_id = open_debit_card_account_data["account"]["cards"][0]["id"]
    make_top_up_operation_body = {
        "status": "COMPLETED",
        "amount": 5550,
        "cardId": card_id,
        "accountId": account_id,
    }
    # Пополнение счёта дебитовой карты
    make_top_up_operation_response = client.post(
        "/operations/make-top-up-operation", json=make_top_up_operation_body
    )
    make_top_up_operation_response.raise_for_status()
    make_top_up_operation_data = make_top_up_operation_response.json()

    print(
        f"Top up operation:\n{json.dumps(make_top_up_operation_data, indent=2, ensure_ascii=False)}"
    )
