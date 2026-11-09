from selenium.webdriver.common.by import By

from zags.pages.base_page import BasePage
from zags.pages.status_page import StatusPage


class DataPage(BasePage):
    TITLE = (By.XPATH, '//label[contains(., "Новая фамилия")]')
    REG_DATA = (By.XPATH, '//label[contains(., "Дата регистрации")]/following::input[1]')
    NEW_SURNAME = (By.XPATH, '//label[contains(., "Новая фамилия")]/following::input[1]')
    SURNAME_SUP = (By.XPATH, '//label[contains(., "Фамилия супруга")]/following::input[1]')
    NAME_SUP = (By.XPATH, '//label[contains(., "Имя супруга")]/following::input[1]')
    LASTNAME_SUP = (By.XPATH, '//label[contains(., "Отчество супруга")]/following::input[1]')
    BIRTH_DATE = (By.XPATH, '//label[contains(., "Дата рождения супруга")]/following::input[1]')
    PASPORT = (By.XPATH, '//label[contains(., "Номер паспорта супруга")]/following::input[1]')
    FINISH_BUTTON = (By.XPATH, '//button[normalize-space(.)="Завершить"]')

    def wait_until_open(self):
        self.visible(self.TITLE)

    def fill_reg_data(self, value: str):
        self.fill_date(self.REG_DATA, value)

    def fill_new_surname(self, value: str):
        field = self.visible(self.NEW_SURNAME)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_surname_sup(self, value: str):
        field = self.visible(self.SURNAME_SUP)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_name_sup(self, value: str):
        field = self.visible(self.NAME_SUP)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_lastname_sup(self, value: str):
        field = self.visible(self.LASTNAME_SUP)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_birth_date(self, value: str):
        self.fill_date(self.BIRTH_DATE, value)

    def fill_pasport(self, value: str):
        field = self.visible(self.PASPORT)
        field.click()
        field.clear()
        field.send_keys(value)

    def click_finish(self):
        self.click(self.FINISH_BUTTON)
        page = StatusPage(self.driver, self.timeout)
        page.wait_until_open()
        return page
