from selenium.webdriver.common.by import By

from zags.pages.base_page import BasePage
from zags.pages.Citizen_data import CitizenData
from zags.pages.citizen_page import CitizenPage


class Application_choice(BasePage):
    DIALOG = (By.CSS_SELECTOR, '[role="dialog"]')
    BUTTON = (By.XPATH, '//*[@role="dialog"]//button[normalize-space(.)="Регистрация рождения"]')
    WEDDING_BUTTON = (
        By.XPATH,
        '//*[@role="dialog"]//button[normalize-space(.)="Регистрация брака"]',
    )
    CHOSENAPP = (By.XPATH, '//*[contains(text(), "услугу")]')

    def wait_until_open(self):
        self.visible(self.BUTTON)

    def button_is_enabled(self):
        return self.visible(self.BUTTON).is_enabled()

    def birthapp_choice(self):
        self.click(self.BUTTON)
        page = CitizenData(self.driver, self.timeout)
        page.wait_until_open()
        return page

    def wedding_choice(self):
        self.click(self.WEDDING_BUTTON)
        page = CitizenPage(self.driver, self.timeout)
        page.wait_until_open()
        return page
