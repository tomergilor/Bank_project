"""
Shared pytest fixtures placeholder.
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tests.ui.pages.dashboard_page import DashboardPage
from tests.ui.pages.login_page import LoginPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")


    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_dashboard(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.open()
    login_page.login("tomer_admin", "Admin123")
    dashboard_page.wait_until_loaded()

    return dashboard_page