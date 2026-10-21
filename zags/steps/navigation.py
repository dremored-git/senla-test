from selenium.webdriver.remote.webdriver import WebDriver

from zags.pages.home_page import HomePage
from zags.settings import Settings


def open_zags(driver: WebDriver, settings: Settings) -> HomePage:
    return HomePage(driver, settings.timeout).open(settings)
