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


    def surname_value(self):
            return self.visible(self.SURNAME).get_property("value")

    def fill_name(self, value: str):
        field = self.visible(self.NAME)
        field.click()
        field.clear()
        field.send_keys(value)

    def name_value(self):
           return self.visible(self.NAME).get_property("value")

    def fill_lastname(self, value: str):
        field = self.visible(self.LASTNAME)
        field.click()
        field.clear()
        field.send_keys(value)


    def lastname_value(self):
            return self.visible(self.LASTNAME).get_property("value")

    def fill_telephon(self, value: str):
        field = self.visible(self.TELEPHON)
        field.click()
        field.clear()
        field.send_keys(value)


    def telephon_value(self):
            return self.visible(self.TELEPHON).get_property("value")

    def fill_pasport(self, value: str):
        field = self.visible(self.PASPORT)
        field.click()
        field.clear()
        field.send_keys(value)


    def pasport_value(self):
            return self.visible(self.PASPORT).get_property("value")

    def fill_address(self, value: str):
        field = self.visible(self.ADDRESS)
        field.click()
        field.clear()
        field.send_keys(value)


    def address_value(self):
            return self.visible(self.ADDRESS).get_property("value")

    def click_next(self):
        self.click(self.NEXT_BUTTON)

    def click_brak(self):
        self.click(self.BRAK_BUTTON)
        
    def close(self):
        self.click(self.CLOSE_BUTTON)