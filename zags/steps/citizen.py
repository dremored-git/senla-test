<<<<<<< HEAD
from zags.pages.application_choice import Application_choice
from zags.pages.Citizen_data import CitizenData


def open_app_citizen_form(home_page: Application_choice) -> CitizenData:
    return home_page.birtapp_choice()


def fill_citizen_surname(page: CitizenData, value: str) -> None:
    page.set_surname(value)


def fill_citizen_firstname(page: CitizenData, value: str) -> None:
    page.set_firstname(value)


def fill_citizen_lastname(page: CitizenData, value: str) -> None:
    page.set_lastname(value)


def fill_citizen_birthdate(page: CitizenData, value: str) -> None:
    page.set_birthdate(value)


def fill_citizen_passport(page: CitizenData, value: str) -> None:
    page.set_passport(value)


def fill_citizen_gender(page: CitizenData, value: str) -> None:
    page.set_gender(value)


def fill_user_adress(page: CitizenData, value: str) -> None:
    page.set_adress(value)


def check_required_fields_filled(page: CitizenData, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value != "" for value in actual), "Some required fields are empty"


def check_next_button_enabled(page: CitizenData, expected: bool) -> None:
    actual = page.next_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"


def next_to_applicationdata(page: CitizenData) -> None:
    page.next()


def close_citizen_form(page: CitizenData) -> None:
    page.close()


def check_citizen_form_closed(page: CitizenData) -> None:
    assert not page.is_open(), "Citizen dialog is still open"
=======
from zags.pages.citizen_page import CitizenPage


def fill_citizen_data(page: CitizenPage, birth_date: str, address: str) -> None:
    page.fill_birth_date(birth_date)
    page.fill_address(address)

def click_next_on_citizen(page: CitizenPage) -> None:
    page.click_next()
>>>>>>> origin/main
