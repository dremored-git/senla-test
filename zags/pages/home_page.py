from selenium.webdriver.common.by import By

from zags.pages.admin_page import AdminPage
from zags.pages.base_page import BasePage


class HomePage(BasePage):
    ENTER_ADMIN = (By.XPATH, '//button[normalize-space(.)="Войти как администратор"]')

    def open(self, settings):
        # This training stand uses HTTP Basic Auth before its application UI.
        self.driver.get(settings.authenticated_url())
        self.visible(self.ENTER_ADMIN)
        return self

    def open_admin(self):
        self.click(self.ENTER_ADMIN)
        page = AdminPage(self.driver, self.timeout)
        page.wait_until_open()
        return page
