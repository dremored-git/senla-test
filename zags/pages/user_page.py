from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zags.pages.base_page import BasePage


class UserPage (BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    FIELDS = (By.CSS_SELECTOR, '[role="dialog"] input[required]')
    APPCHOICE = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Регистрация брака"]')
    SURNAME = (
        By.XPATH,
        '//input[@placeholder="Введите фамилию (минимум 2 символа)"]',
    )
    FIRSTNAME = (
         By.XPATH,
        '//input[@placeholder="Введите имя (минимум 2 символа)"]'
    )
    THIRDNAME = (
         By.XPATH,
        '//input[@placeholder="Введите отчество (минимум 5 символов)"]'
    )
    PHONE = (
        By.XPATH,
        '//input[@placeholder="Введите номер телефона (не более 11 символов)"]'
    )
    PASSPORT = (
        By.XPATH,
        '//input[@placeholder="Введите номер паспорта (не более 8 символов)"]'
    )
    ADRESS = (
        By.XPATH,
        '//input[@placeholder="Введите адрес прописки"]'
    )
    NEXT = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Далее"]')
    CLOSE = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Закрыть"]')

    def wait_until_open(self):
        self.visible(self.DIALOG)

    def required_values(self):
        self.wait.until(EC.presence_of_all_elements_located(self.FIELDS))
        return [field.get_property("value") for field in self.driver.find_elements(*self.FIELDS)]

    def next_is_enabled(self):
        return self.visible(self.NEXT).is_enabled()

    def set_surname(self, value):
        field = self.visible(self.SURNAME)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.SURNAME).get_property("value") == value
        )

    def surname_value(self):
        return self.visible(self.SURNAME).get_property("value")
        

    def set_firstname(self,value):
        field=self.visible(self.FIRSTNAME)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.FIRSTNAME).get_property("value") == value
                )


    def firstname_value(self):
        return self.visible(self.FIRSTNAME).get_property("value")



    def set_thirdname(self,value):
        field=self.visible(self.THIRDNAME)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.THIRDNAME).get_property("value") == value
                )
    def thirdname_value(self):
        return self.visible(self.THIRDNAME).get_property("value")


    def set_phone(self,value):
            field=self.visible(self.PHONE)
            field.clear()
            if value:
                field.send_keys(value)
            self.wait.until(
                lambda driver: driver.find_element(*self.PHONE).get_property("value") == value
                    )

    def phone_value(self):
            return self.visible(self.PHONE).get_property("value")



    def set_passport(self,value):
            field=self.visible(self.PASSPORT)
            field.clear()
            if value:
                field.send_keys(value)
            self.wait.until(
                lambda driver: driver.find_element(*self.PASSPORT).get_property("value") == value
                    )

    def passport_value(self):
                return self.visible(self.PASSPORT).get_property("value")


    def set_adress(self,value):
        field=self.visible(self.ADRESS)
        field.clear()
        if value:
           field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.ADRESS).get_property("value") == value
                )


    def adress_value(self):
                return self.visible(self.ADRESS).get_property("value")

    
    def close(self):
        self.click(self.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(self.DIALOG))


    def next(self):
        self.click(self.NEXT)
        self.wait.until(EC.visibility_of_element_located(self.APPCHOICE))

    def is_open(self):
        return any(element.is_displayed() for element in self.driver.find_elements(*self.DIALOG))
