import re
from datetime import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @staticmethod
    def normalize_date(value: str) -> str:
        """Accept ISO or legacy day-first dates; reject invalid calendar dates."""
        if value == "":
            return ""
        formats = ((r"\d{4}-\d{2}-\d{2}", "%Y-%m-%d"),
                   (r"\d{2}\.\d{2}\.\d{4}", "%d.%m.%Y"),
                   (r"\d{2}-\d{2}-\d{4}", "%d-%m-%Y"))
        for pattern, date_format in formats:
            if re.fullmatch(pattern, value):
                return datetime.strptime(value, date_format).date().isoformat()
        raise ValueError("Expected YYYY-MM-DD, DD.MM.YYYY or DD-MM-YYYY")

    def fill_date(self, locator, value: str) -> None:
        normalized = self.normalize_date(value)
        field = self.visible(locator)
        self.driver.execute_script(
            """
            const field = arguments[0];
            const view = field.ownerDocument.defaultView;
            const setter = Object.getOwnPropertyDescriptor(
                view.HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(field, arguments[1]);
            field.dispatchEvent(new view.Event('input', {bubbles: true}));
            field.dispatchEvent(new view.Event('change', {bubbles: true}));
            """,
            field,
            normalized,
        )
        self.wait.until(
            lambda driver: driver.find_element(*locator).get_property("value") == normalized
        )
