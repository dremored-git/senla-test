from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zags.pages.base_page import BasePage


class CitizenData (BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    FIELDS = (By.CSS_SELECTOR, '[role="dialog"] input[required]')
    BIRTHAPP = (By.XPATH, '//label[contains(., "Место рождения")]/following::input[1]')
    LASTNAME = (
        By.XPATH,
        '//label[contains(., "Фамилия")]/following::input[1]',
    )
    FIRSTNAME = (
         By.XPATH,
        '//label[contains(., "Имя")]/following::input[1]'
    )
    SURNAME = (
         By.XPATH,
        '//label[contains(., "Отчество")]/following::input[1]'
    )
    BIRTHDATE = (
        By.XPATH,
        '//label[contains(., "Дата рождения")]/following::input[1]'
    )
    PASSPORT = (
        By.XPATH,
        '//label[contains(., "Номер паспорта")]/following::input[1]'
    )
    GENDER = ( 
         By.XPATH,
        '//label[contains(., "Пол")]/following::input[1]'
    )
    ADRESS = (
        By.XPATH,
        '//label[contains(., "Адрес прописки")]/following::input[1]'
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



    def set_lastname(self,value):
        field=self.visible(self.LASTNAME)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.LASTNAME).get_property("value") == value
                )
    def lastname_value(self):
        return self.visible(self.LASTNAME).get_property("value")


    def set_birthdate(self,value):
            field=self.visible(self.BIRTHDATE)
            field.clear()
            if value:
                field.send_keys(value)
            #self.wait.until(
                #lambda driver: driver.find_element(*self.BIRTHDATE).get_property("value") == value
                    #)


    def birthdate_value(self):
        return self.visible(self.BIRTHDATE).get_property("value")


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


    def set_gender(self,value):
                field=self.visible(self.GENDER)
                field.clear()
                if value:
                    field.send_keys(value)
                self.wait.until(
                    lambda driver: driver.find_element(*self.GENDER).get_property("value") == value
                        )
    
    def gender_value(self):
              return self.visible(self.GENDER).get_property("value")


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
        self.wait.until(EC.visibility_of_element_located(self.BIRTHAPP))

    def is_open(self):
        return any(element.is_displayed() for element in self.driver.find_elements(*self.DIALOG))