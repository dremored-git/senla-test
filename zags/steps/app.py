from zags.pages.appdata import AppData
from zags.pages.Citizen_data import CitizenData


def open_app_data_form(home_page: CitizenData) -> AppData:
    return home_page.next()


def fill_app_birthblase(page: AppData, value: str) -> None:
    page.set_birthplace(value)


def fill_app_mother(page: AppData, value: str) -> None:
    page.set_mother(value)


def fill_app_father(page: AppData, value: str) -> None:
    page.set_father(value)


def fill_app_grandmother(page: AppData, value: str) -> None:
    page.set_grandmother(value)


def fill_app_grandfather(page: AppData, value: str) -> None:
    page.set_grandfather(value)


def check_required_fields_filled(page: AppData, expected_count: int) -> None:
    actual = page.required_values()
    assert len(actual) == expected_count, (
        f"Required fields: expected {expected_count}, got {len(actual)}"
    )
    assert all(value != "" for value in actual), "Some required fields are empty"


def check_finish_button_enabled(page: AppData, expected: bool) -> None:
    actual = page.finish_is_enabled()
    assert actual == expected, f"Next button enabled: expected {expected}, got {actual}"


def next_to_applicationstatus(page: AppData) -> None:
    page.finish()


def check_citizen_form_closed(page: AppData) -> None:
    assert not page.is_open(), "AppData dialog is still open"
