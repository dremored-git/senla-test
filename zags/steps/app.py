import allure

from zags.pages.appdata import AppData
from zags.pages.Citizen_data import CitizenData
from zags.pages.statusapp import AppStatuspage


@allure.step("Открыть форму услуги")
def open_app_data_form(home_page: CitizenData) -> AppData:
    return home_page.next()

@allure.step("Заполнить место рождения")
def fill_app_birthblase(page: AppData, value: str) -> None:
    page.set_birthplace(value)

@allure.step("Заполнить данные о матери")
def fill_app_mother(page: AppData, value: str) -> None:
    page.set_mother(value)

@allure.step("Заполнить данные об отце")
def fill_app_father(page: AppData, value: str) -> None:
    page.set_father(value)

@allure.step("заполнить данные о бабушке")
def fill_app_grandmother(page: AppData, value: str) -> None:
    page.set_grandmother(value)

@allure.step("Заполнить данные о дедушке")
def fill_app_grandfather(page: AppData, value: str) -> None:
    page.set_grandfather(value)

@allure.step("Проверить,что обязательные поля заполнены")
def check_required_fields_filled(page: AppData, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value != "" for value in actual), "Some required fields are empty"

@allure.step("Проверить, что кнопка 'Завершить'доступна")
def check_finish_button_enabled(page: AppData, expected: bool) -> None:
    actual = page.finish_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"

@allure.step("Перейти на страницу статуса заявки")
def next_to_applicationstatus(page: AppData) -> AppStatuspage:
    return page.finish()

@allure.step("Проверить, что форма 'Данные гражданина' закрыта")
def check_citizen_form_closed(page: AppData) -> None:
    assert not page.is_open(), "AppData dialog is still open"
