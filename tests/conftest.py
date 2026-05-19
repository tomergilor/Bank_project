"""
Shared pytest fixtures placeholder.
"""
import threading
import time

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from werkzeug.serving import make_server

from app.server import app
from tests.ui.pages.dashboard_page import DashboardPage
from tests.ui.pages.login_page import LoginPage


class TestServerThread(threading.Thread):
    def __init__(self, host: str = "127.0.0.1", port: int = 5000):
        super().__init__(daemon=True)
        self.server = make_server(host, port, app)
        self.context = app.app_context()
        self.context.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.context.pop()


@pytest.fixture(scope="session", autouse=True)
def live_server():
    server_thread = TestServerThread()
    server_thread.start()

    health_url = "http://127.0.0.1:5000/api/health"
    last_error = None
    for _ in range(50):
        try:
            response = requests.get(health_url, timeout=1)
            if response.status_code == 200:
                break
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(0.1)
    else:
        server_thread.shutdown()
        raise RuntimeError(f"Failed to start test server on {health_url}") from last_error

    yield
    server_thread.shutdown()


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
