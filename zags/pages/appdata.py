from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zags.pages.base_page import BasePage


class AppData(BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    FIELDS = (By.CSS_SELECTOR, '[role="dialog"] input[required]')
    APPSTATUS = (By.XPATH, '//button[contains(text(), "Обновить")]')
    BIRTHPLACE = (By.CSS_SELECTOR, ('input[type="text"][required][id^="TextInputField-"]'))
    MOTHER = (By.XPATH, '//input[@id=//label[starts-with(text(), "Ма")]/@for]')
    FATHER = (By.XPATH, '//input[@id=//label[starts-with(text(), "От")]/@for]')
    GRANDMOTHER = (By.XPATH, '//input[@id=//label[starts-with(text(), "Ба")]/@for]')
    GRANDFATHER = (By.XPATH, '//input[@id=//label[starts-with(text(), "Де")]/@for]')

    FINISH = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Завершить"]')
    CLOSE = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Закрыть"]')

    def wait_until_open(self):
        self.visible(self.DIALOG)

    def required_values(self):
        self.wait.until(EC.presence_of_all_elements_located(self.FIELDS))
        return [field.get_property("value") for field in self.driver.find_elements(*self.FIELDS)]

    def finish_is_enabled(self):
        return self.visible(self.FINISH).is_enabled()

    def set_birthplace(self, value):
        field = self.visible(self.BIRTHPLACE)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.BIRTHPLACE).get_property("value") == value
        )

    def birthplace_value(self):
        return self.visible(self.BIRTHPLACE).get_property("value")

    def set_mother(self, value):
        field = self.visible(self.MOTHER)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.MOTHER).get_property("value") == value
        )

    def mother_value(self):
        return self.visible(self.MOTHER).get_property("value")

    def set_father(self, value):
        field = self.visible(self.FATHER)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.FATHER).get_property("value") == value
        )

    def father_value(self):
        return self.visible(self.FATHER).get_property("value")

    def set_grandmother(self, value):
        field = self.visible(self.GRANDMOTHER)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.GRANDMOTHER).get_property("value") == value
        )

    def grandmother_value(self):
        return self.visible(self.GRANDMOTHER).get_property("value")

    def set_grandfather(self, value):
        field = self.visible(self.GRANDFATHER)
        field.clear()
        if value:
            field.send_keys(value)
        self.wait.until(
            lambda driver: driver.find_element(*self.GRANDFATHER).get_property("value") == value
        )

    def grandfather_value(self):
        return self.visible(self.GRANDFATHER).get_property("value")

    def finish(self):
        self.click(self.FINISH)
        self.wait.until(EC.visibility_of_element_located(self.APPSTATUS))

    def is_open(self):
        return any(element.is_displayed() for element in self.driver.find_elements(*self.DIALOG))
