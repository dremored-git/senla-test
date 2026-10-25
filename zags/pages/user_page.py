from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zags.pages.base_page import BasePage


class UserPage (BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    FIELDS = (By.CSS_SELECTOR, '[role="dialog"] input[required]')
    SURNAME = (
        By.XPATH,
        '//*[@id="TextInputField-1"]',
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

    def close(self):
        self.click(self.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(self.DIALOG))

    def is_open(self):
        return any(element.is_displayed() for element in self.driver.find_elements(*self.DIALOG))
