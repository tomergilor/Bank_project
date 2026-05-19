
import pytest

from tests.ui.pages.login_page import LoginPage
from tests.test_data import VALID_USER


pytestmark = pytest.mark.ui


def test_login_success(logged_in_dashboard, driver):
    assert "dashboard" in driver.current_url


def test_role_and_status_correct(logged_in_dashboard):
    assert logged_in_dashboard.get_welcome_message() == "Welcome, Tomer Gil-Or"
    assert logged_in_dashboard.get_role_info() == "Role: admin"
    assert logged_in_dashboard.get_active_status() == "Active: True"


def test_account_information(logged_in_dashboard):
    assert logged_in_dashboard.get_account_number() == "100200300"
    assert logged_in_dashboard.get_balance_amount() == "15420.75 ILS"


def test_login_failed(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("wrong_user", VALID_USER["password"])

    assert login_page.get_error_message() == "Invalid username or password."
