import allure

from zags.pages.appdata import AppData
from zags.pages.application_choice import Application_choice
from zags.pages.Citizen_data import CitizenData
from zags.pages.citizen_page import CitizenPage
from zags.pages.data_page import DataPage


def open_app_citizen_form(home_page: Application_choice) -> CitizenData:
    return home_page.birthapp_choice()


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


def next_to_applicationdata(page: CitizenData) -> AppData:
    return page.next()


def close_citizen_form(page: CitizenData) -> None:
    page.close()


def check_citizen_form_closed(page: CitizenData) -> None:
    assert not page.is_open(), "Citizen dialog is still open"


@allure.step("Заполнить данные гражданина")
def fill_citizen_data(page: CitizenPage, birth_date: str, address: str) -> None:
    page.fill_data(birth_date)
    page.fill_address(address)


@allure.step("Перейти на следующий шаг")
def click_next_on_citizen(page: CitizenPage) -> DataPage:
    return page.click_next()


@allure.step("Заполнить фамилию гражданина")
def fill_citizen_family_name(page: CitizenData, value: str) -> None:
    page.set_lastname(value)


@allure.step("Заполнить отчество гражданина")
def fill_citizen_patronymic(page: CitizenData, value: str) -> None:
    page.set_surname(value)


@allure.step("Заполнить данные гражданина для регистрации брака")
def fill_wedding_citizen_data(
    page: CitizenPage, family_name: str, name: str, patronymic: str,
    birth_date: str, passport: str, gender: str, address: str,
) -> None:
    page.fill_surname(family_name)
    page.fill_name(name)
    page.fill_lastname(patronymic)
    page.fill_data(birth_date)
    page.fill_pasport(passport)
    page.fill_gender(gender)
    page.fill_address(address)
