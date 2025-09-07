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

    account_id = open_credit_card_account_data["account"]["id"]

    # Получение тарифного документа
    get_tariff_document_response = client.get(f"/documents/tariff-document/{account_id}")
    get_tariff_document_response.raise_for_status()
    get_tariff_document_data = get_tariff_document_response.json()
    
    print(f"Tariff document data:\n{json.dumps(get_tariff_document_data, indent=2, ensure_ascii=False)}")

    # Получение договорного документа (убрал дублирование /api/v1)
    get_contract_document_response = client.get(f"/documents/contract-document/{account_id}")
    get_contract_document_response.raise_for_status()
    get_contract_document_data = get_contract_document_response.json()
    
    print(f"Contract document data:\n{json.dumps(get_contract_document_data, indent=2, ensure_ascii=False)}")