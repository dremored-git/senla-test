from zags.pages.home_page import HomePage
from zags.pages.user_page import UserPage
import allure

@allure.step("Открыть форму пользователя")
def open_user_form(home_page: HomePage) -> UserPage:
    return home_page.open_user()