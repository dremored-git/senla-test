from zags.pages.user_page import UserPage
from zags.pages.home_page import HomePage
from zags.pages.application_choice import Application_choice

def open_user_form(home_page: HomePage) -> UserPage:
    return home_page.open_user()


def fill_user_surname(page: UserPage, value: str) -> None:
    page.set_surname(value)


def fill_user_firstname(page: UserPage, value: str) -> None:
    page.set_firstname(value)


def fill_user_thirdname(page: UserPage, value: str) -> None:
    page.set_thirdname(value)


def fill_user_phone(page: UserPage, value: str) -> None:
    page.set_phone(value)


def fill_user_passport(page: UserPage, value: str) -> None:
    page.set_passport(value)


def fill_user_adress(page: UserPage, value: str) -> None:
    page.set_adress(value)


def check_user_surname(page: UserPage, expected: str) -> None:
    actual = page.surname_value()
    assert actual == expected, f"Surname: expected {expected!r}, got {actual!r}"


def check_required_fields_empty(page: UserPage, expected_count:int) -> None:
    actual=page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
        )
    assert all(value == "" for value in actual), "Some required fields are not empty"

def check_required_fields_are_not_empty(page: UserPage, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value != "" for value in actual), "Some required fields are empty"


def check_next_button_enabled(page: UserPage, expected: bool) -> None:
    actual = page.next_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"


def next_to_application (page: UserPage) -> None:
    page.next()


def birtapp_choice (page: Application_choice) -> None:
    page.birtapp_choice()


def close_user_form(page: UserPage) -> None:
    page.close()


def check_user_form_closed(page: UserPage) -> None:
    assert not page.is_open(), "User dialog is still open"