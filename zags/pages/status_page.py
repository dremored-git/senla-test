import re

from selenium.webdriver.common.by import By

from zags.pages.base_page import BasePage


class StatusPage(BasePage):
    TITLE = (By.XPATH, '//*[contains(text(), "Статус заявки")]')
    APP_NUMBER_TEXT = (By.XPATH, '//*[contains(text(), "Ваша заявка №")]')
    STATUS_TEXT = (By.XPATH, '//*[contains(text(), "Статус заявки:")]')

    def wait_until_open(self):
        self.visible(self.TITLE) 

    def get_application_number(self) -> str:
        full_text = self.visible(self.APP_NUMBER_TEXT).text
        numbers = re.findall(r'\d+', full_text)
        return numbers[0] if numbers else ""

    def get_status(self) -> str:
        full_text = self.visible(self.STATUS_TEXT).text
        status = full_text.replace("Статус заявки:", "").strip()
        return status