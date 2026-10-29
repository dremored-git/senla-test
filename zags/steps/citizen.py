import allure

from zags.pages.citizen_page import CitizenPage


@allure.step("Заполнить данные гражданина")
def fill_citizen_data(page: CitizenPage, birth_date: str, address: str) -> None:
    page.fill_birth_date(birth_date)
    page.fill_address(address)
    
@allure.step("Перейти на следующий шаг")
def click_next_on_citizen(page: CitizenPage) -> None:
    page.click_next()