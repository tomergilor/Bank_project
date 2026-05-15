"""
Login page object placeholder.
"""

from selenium.webdriver.common.by import By

from tests.ui.pages.base_page import BasePage
from tests.config import BASE_URL


class LoginPage(BasePage):

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON =   (By.ID, "login-button")
    ERROR_MESSAGE = (By.ID, "error-message")


    def open(self):
        self.driver.get(BASE_URL)


    def insert_username(self, username):
        self.type(self.USERNAME_INPUT, username)


    def insert_password(self, password):
        self.type(self.PASSWORD_INPUT, password)


    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)


    def login(self, username, password):
        self.insert_username(username)
        self.insert_password(password)
        self.click_login_button()


    def get_error_message(self):
        return self.wait_for_visible(self.ERROR_MESSAGE).text
