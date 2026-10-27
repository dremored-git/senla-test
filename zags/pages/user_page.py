from selenium.webdriver.common.by import By

from zags.pages.base_page import BasePage


class UserPage(BasePage):

    TITLE = (By.CSS_SELECTOR, 'div[role="dialog"]')
    SURNAME = (By.XPATH, '//input[contains(@placeholder, "Введите фамилию")]')
    NAME = (By.XPATH, '//input[contains(@placeholder, "Введите имя")]')
    LASTNAME = (By.XPATH, '//input[contains(@placeholder, "Введите отчество")]')
    TELEPHON = (By.XPATH, '//input[contains(@placeholder, "телефон")]')
    PASPORT = (By.XPATH, '//input[contains(@placeholder, "паспорт")]')
    ADDRESS = (By.XPATH, '//input[contains(@placeholder, "Введите адрес прописки")]')
    NEXT_BUTTON = (By.XPATH, '//button[contains(normalize-space(.), "Далее")]') 
    BRAK_BUTTON = (By.XPATH, '//button[contains(normalize-space(.), "Регистрация брака")]')
    CLOSE_BUTTON = (By.XPATH, '//button[contains(normalize-space(.), "Закрыть")]')

    def wait_until_open(self):
        self.visible(self.TITLE)

    def fill_surname(self, value: str):
        field = self.visible(self.SURNAME)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_name(self, value: str):
        field = self.visible(self.NAME)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_lastname(self, value: str):
        field = self.visible(self.LASTNAME)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_telephon(self, value: str):
        field = self.visible(self.TELEPHON)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_pasport(self, value: str):
        field = self.visible(self.PASPORT)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_address(self, value: str):
        field = self.visible(self.ADDRESS)
        field.click()
        field.clear()
        field.send_keys(value)

    def click_next(self):
        self.click(self.NEXT_BUTTON)

    def click_brak(self):
        self.click(self.BRAK_BUTTON)
        
    def close(self):
        self.click(self.CLOSE_BUTTON)
    