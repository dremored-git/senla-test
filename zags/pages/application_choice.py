from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from zags.pages.base_page import BasePage


class Application_choice(BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    BUTTON = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Регистрация рождения"]')
    CHOSENAPP = (By.XPATH, '//*[contains(text(), "услугу")]')

    def wait_until_open(self):
        self.visible(self.DIALOG)

    def button_is_enabled(self):
        return self.visible(self.BUTTON).is_enabled()

    def birthapp_choice(self):
        self.click(self.BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.CHOSENAPP))
