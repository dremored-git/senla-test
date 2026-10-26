from selenium.webdriver.common.by import By

from zags.pages.base_page import BasePage


class CitizenPage(BasePage):
    TITLE = (By.XPATH, '//*[contains(text(), "Данные гражданина")]') 
    SURNAME = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[1]')
    NAME = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[2]')
    LASTNAME = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[3]')
    DATA = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[4]') 
    PASPORT = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[5]')
    GENDER = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[6]')
    ADDRESS = (By.XPATH, '(//div[contains(@class, "ub-mb_24px")]//input)[7]')
    NEXT_BUTTON = (By.XPATH, '//button[normalize-space(.)="Далее"]')

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

    def fill_data(self, value: str):
        field = self.visible(self.DATA)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_pasport(self, value: str):
        field = self.visible(self.PASPORT)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_gender(self, value: str):
        field = self.visible(self.GENDER)
        field.click()
        field.clear()
        field.send_keys(value)

    def fill_address(self, value: str):
        field = self.visible(self.ADDRESS)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field) 
        field.click()
        field.clear()
        field.send_keys(value)
  
    def click_next(self):
        self.click(self.NEXT_BUTTON)