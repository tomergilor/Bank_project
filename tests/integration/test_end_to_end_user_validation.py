import pytest
import requests
import sqlite3
from pathlib import Path

from tests.ui.pages.dashboard_page import DashboardPage
from tests.ui.pages.login_page import LoginPage
from tests.config import BASE_URL
from tests.test_data import VALID_USER


DB_PATH = Path(__file__).resolve().parents[2] / "app" / "data" / "bank.db"

pytestmark = pytest.mark.integration


def test_user_data_consistency_across_ui_api_and_db(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.open()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    dashboard_page.wait_until_loaded()

    ui_welcome_message = dashboard_page.get_welcome_message()
    assert ui_welcome_message == "Welcome, Tomer Gil-Or"


    ## API test:
    api_response = requests.get(f"{BASE_URL}/api/users/tomer_admin")

    response_body = api_response.json()
    print(response_body)


    ## Check API data
    assert api_response.status_code == 200
    assert response_body["success"] is True

    assert "accounts" in response_body
    assert len(response_body["accounts"]) > 0

    first_account = response_body["accounts"][0]

    assert first_account["account_number"] == "100200300"
    assert first_account["account_type"] == "checking"
    assert first_account["balance"] == 15420.75
    assert first_account["currency"] == "ILS"



    ## DB Test
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT username, first_name, last_name, role, is_active
        FROM users
        WHERE username = ?
        """,
        (VALID_USER["username"],)
    )

    db_user = cursor.fetchone()

    ## Check DB data
    assert db_user is not None
    assert db_user["username"] == VALID_USER["username"]
    assert db_user["first_name"] == "Tomer"
    assert db_user["last_name"] == "Gil-Or"
    assert db_user["is_active"] == True
    assert db_user["role"] == "admin"
    assert db_user["is_active"] == 1


    ## Check API=DB
    assert response_body["user"]["username"] == db_user["username"]
    assert response_body["user"]["first_name"] == db_user["first_name"]
    assert response_body["user"]["last_name"] == db_user["last_name"]
    assert response_body["user"]["role"] == db_user["role"]


