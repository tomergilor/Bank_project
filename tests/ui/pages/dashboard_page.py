"""
Dashboard page object placeholder.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:

    LOGOUT_BUTTON = (By.ID, "logout-link")
    WELCOME_MESSAGE = (By.ID, "welcome-banner")
    ROLE_INFO = (By.ID, "user-role")
    ACTIVE_STATUS = (By.ID, "user-status")
    ACCOUNT_NUMBER = (By.CSS_SELECTOR, ".account-number")
    BALANCE_AMOUNT = (By.CSS_SELECTOR, ".balance-amount")


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_until_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.WELCOME_MESSAGE))

    def click_logout_button(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def get_welcome_message(self):
        self.wait_until_loaded()
        return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def get_role_info(self):
        self.wait_until_loaded()
        return self.driver.find_element(*self.ROLE_INFO).text

    def get_active_status(self):
        self.wait_until_loaded()
        return self.driver.find_element(*self.ACTIVE_STATUS).text

    def get_account_number(self):
        self.wait_until_loaded()
        return self.driver.find_element(*self.ACCOUNT_NUMBER).text

    def get_balance_amount(self):
        self.wait_until_loaded()
        return self.driver.find_element(*self.BALANCE_AMOUNT).text