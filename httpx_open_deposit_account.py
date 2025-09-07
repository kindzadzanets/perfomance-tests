import httpx
from random import randint

with httpx.Client(base_url="http://localhost:8003", timeout=10) as c:
    create_user_body = {
        "email": f"httpx_user_{randint(0, 1000)}@example.com",
        "lastName": "user",
        "firstName": "httpx",
        "middleName": "none",
        "phoneNumber": "+48291293",
    }

    created_user_response = c.post("/api/v1/users", json=create_user_body)
    created_user_response.raise_for_status()
    created_user_response_data = created_user_response.json()

    # print(created_user_response.status_code)

    open_deposit_account_body = {"userId": created_user_response_data["user"]["id"]}
    open_deposit_account_response = c.post(
        "/api/v1/accounts/open-deposit-account", json=open_deposit_account_body
    )
    open_deposit_account_response.raise_for_status()
    open_deposit_account_response_data = open_deposit_account_response.json()

    print(
        f"Opened account info: {open_deposit_account_response_data}\nStatus code: {open_deposit_account_response.status_code}"
    )
