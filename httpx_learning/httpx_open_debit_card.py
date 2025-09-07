import httpx
import json
from user_data_generator import generate_user_data

with httpx.Client(base_url="http://localhost:8003", timeout=10) as client:
    created_user_response = client.post("/api/v1/users", json=generate_user_data())
    created_user_response.raise_for_status()
    created_user_response_data = created_user_response.json()

    open_debit_card_account_body = {"userId": created_user_response_data["user"]["id"]}

    open_debit_card_account_response = client.post(
        "/api/v1/accounts/open-debit-card-account", json=open_debit_card_account_body
    )
    open_debit_card_account_response.raise_for_status()
    open_debit_card_account_response_data = open_debit_card_account_response.json()

    print(
        f"Account was successfully opened:\n{json.dumps(open_debit_card_account_response_data, indent=2, ensure_ascii=False)}"
    )

    issue_virtual_card_body = {
        "userId": created_user_response_data["user"]["id"],
        "accountId": open_debit_card_account_response_data["account"]["id"]
    }
    issue_virtual_card_response = client.post(
        "/api/v1/cards/issue-virtual-card", json=issue_virtual_card_body
    )
    issue_virtual_card_response.raise_for_status()
    issue_virtual_card_data = issue_virtual_card_response.json()

    print(
        f"Virtual card was successfully created:\n{json.dumps(issue_virtual_card_data, indent=2, ensure_ascii=False)}"
    )

    get_user_accounts_params = {"userId": created_user_response_data["user"]["id"]}
    get_user_accounts_response = client.get("/api/v1/accounts", params=get_user_accounts_params)
    get_user_accounts_response.raise_for_status()
    get_user_accounts_response_data = get_user_accounts_response.json()

    print(f"User {created_user_response_data["user"]["firstName"]} {created_user_response_data["user"]["lastName"]} account info:\n{json.dumps(get_user_accounts_response_data, indent=2, ensure_ascii=False)}")