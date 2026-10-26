from zags.pages.home_page import HomePage
from zags.pages.user_page import UserPage

def open_user_form(home_page: HomePage) -> UserPage:
    return home_page.open_user()