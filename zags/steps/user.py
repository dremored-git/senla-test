import allure

from zags.pages.home_page import HomePage
from zags.pages.user_page import UserPage


@allure.step("Открыть форму пользователя")
def open_user_form(home_page: HomePage) -> UserPage:
    return home_page.open_user()


@allure.step("Ввести фамилию: {value}")
def fill_user_surname(page: UserPage, value: str) -> None:
    page.fill_surname(value)


@allure.step("Проверить фамилию: {expected}")
def check_user_surname(page: UserPage, expected: str) -> None:
    actual = page.surname_value()
    assert actual == expected, f"Surname: expected {expected!r}, got {actual!r}"


@allure.step("Проверить, что обязательные поля пусты: {expected_count}")
def check_required_fields_empty(page: UserPage, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value == "" for value in actual), "Some required fields are not empty"


@allure.step("Проверить доступность кнопки Далее: {expected}")
def check_next_button_enabled(page: UserPage, expected: bool) -> None:
    actual = page.next_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"


@allure.step("Закрыть форму пользователя")
def close_user_form(page: UserPage) -> None:
    page.close()


@allure.step("Проверить, что форма пользователя закрыта")
def check_user_form_closed(page: UserPage) -> None:
    assert not page.is_open(), "Admin dialog is still open"
