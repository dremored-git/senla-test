import allure

from zags.pages.admin_page import AdminPage
from zags.pages.home_page import HomePage


@allure.step("Открыть форму администратора")
def open_admin_form(home_page: HomePage) -> AdminPage:
    return home_page.open_admin()


@allure.step("Ввести фамилию: {value}")
def fill_admin_surname(page: AdminPage, value: str) -> None:
    page.set_surname(value)


@allure.step("Проверить фамилию: {expected}")
def check_admin_surname(page: AdminPage, expected: str) -> None:
    actual = page.surname_value()
    assert actual == expected, f"Surname: expected {expected!r}, got {actual!r}"


@allure.step("Проверить, что обязательные поля пусты: {expected_count}")
def check_required_fields_empty(page: AdminPage, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value == "" for value in actual), "Some required fields are not empty"


@allure.step("Проверить доступность кнопки Далее: {expected}")
def check_next_button_enabled(page: AdminPage, expected: bool) -> None:
    actual = page.next_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"


@allure.step("Закрыть форму администратора")
def close_admin_form(page: AdminPage) -> None:
    page.close()


@allure.step("Проверить, что форма администратора закрыта")
def check_admin_form_closed(page: AdminPage) -> None:
    assert not page.is_open(), "Admin dialog is still open"
