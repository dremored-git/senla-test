import allure
from selenium.webdriver.remote.webdriver import WebDriver

from zags.pages.home_page import HomePage
from zags.settings import Settings


@allure.step("Открыть ЗАГС")
def open_zags(driver: WebDriver, settings: Settings) -> HomePage:
    return HomePage(driver, settings.timeout).open(settings)
