"""
API login test placeholder.
"""
import pytest
import requests
from tests.config import BASE_URL
from tests.test_data import VALID_USER, INACTIVE_USER

pytestmark = pytest.mark.api


def test_api_login_success():

    response = requests.post(f"{BASE_URL}/api/login",
        json={
            "username": VALID_USER["username"],
            "password": VALID_USER["password"]
        }
    )

    assert response.status_code == 200

    response_body = response.json()
    print(response_body)

    assert response_body["success"] is True
    assert response_body["user"]["username"] == "tomer_admin"
    assert response_body["user"]["last_name"] == "Gil-Or"
    assert response_body["user"]["role"] == "admin"



def test_api_login_failed():
    response = requests.post(
        f"{BASE_URL}/api/login",
        json={
            "username": VALID_USER["username"],
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
    response_body = response.json()
    print(response_body)
    assert response_body["success"] is False
    assert response_body["message"] == "Invalid credentials"


def test_api_login_with_empty_password():

    response = requests.post(f"{BASE_URL}/api/login",
        json={
            "username": "tomer_admin",
            "password": ""
        }
    )

    assert response.status_code == 401

    response_body = response.json()
    print(response_body)

    assert response_body["success"] is False
    assert response_body["message"] == "Invalid credentials"


def test_api_inactive_user():

    response = requests.post(f"{BASE_URL}/api/login",
        json={
            "username": INACTIVE_USER["username"],
             "password": INACTIVE_USER["password"]
        }
    )

    assert response.status_code == 403

    response_body = response.json()
    print(response_body)
    print(response.status_code)

    assert response_body["success"] is False
    assert response_body["message"] == "User is inactive"



def test_api_user_account():

    response = requests.get(f"{BASE_URL}/api/users/tomer_admin")

    response_body = response.json()
    print(response_body)

    assert response.status_code == 200
    assert response_body["success"] is True

    assert "accounts" in response_body

    assert len(response_body["accounts"]) > 0

    first_account = response_body["accounts"][0]

    assert first_account["account_number"] == "100200300"
    assert first_account["account_type"] == "checking"
    assert first_account["balance"] == 15420.75
    assert first_account["currency"] == "ILS"

