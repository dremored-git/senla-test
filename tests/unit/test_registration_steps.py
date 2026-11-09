import runpy
from pathlib import Path
from unittest.mock import call, create_autospec, patch

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from zags.pages.appdata import AppData
from zags.pages.application_choice import Application_choice
from zags.pages.base_page import BasePage
from zags.pages.Citizen_data import CitizenData
from zags.pages.citizen_page import CitizenPage
from zags.pages.data_page import DataPage
from zags.pages.home_page import HomePage
from zags.pages.status_page import StatusPage
from zags.pages.statusapp import AppStatuspage
from zags.pages.user_page import UserPage
from zags.steps import app, citizen, data, user


def page_mock(cls):
    return create_autospec(cls, instance=True, spec_set=True)


@pytest.mark.parametrize("value,expected", [
    ("1990-01-02", "1990-01-02"),
    ("02.01.1990", "1990-01-02"),
    ("02-01-1990", "1990-01-02"),
    ("29.02.2024", "2024-02-29"),
    ("", ""),
])
def test_normalize_date(value, expected):
    assert BasePage.normalize_date(value) == expected


@pytest.mark.parametrize("value", [
    "2023-02-29", "31.04.2026", "2026-13-01", "01/02/2026", "2026-1-02", "garbage",
])
def test_invalid_dates_fail_before_browser_access(value):
    driver = page_mock(WebDriver)
    with pytest.raises(ValueError):
        BasePage(driver).fill_date(("id", "date"), value)
    driver.find_element.assert_not_called()
    driver.execute_script.assert_not_called()


def test_fill_date_sets_normalized_value_and_waits_for_dom_state():
    driver = page_mock(WebDriver)
    field = page_mock(WebElement)
    field.is_displayed.return_value = True
    field.get_property.side_effect = ["", "2024-02-29"]
    driver.find_element.return_value = field
    page = BasePage(driver, timeout=1)
    page.wait._poll = 0  # No delay for the simulated React update.
    page.fill_date(("id", "date"), "29.02.2024")
    script, target, value = driver.execute_script.call_args.args
    assert target is field
    assert value == "2024-02-29"
    assert "HTMLInputElement.prototype" in script
    assert "setter.call(field, arguments[1])" in script
    assert "Event('input', {bubbles: true})" in script
    assert "Event('change', {bubbles: true})" in script
    assert field.get_property.call_args_list == [call("value"), call("value")]
    field.send_keys.assert_not_called()


@pytest.mark.parametrize("cls,method,locator", [
    (CitizenData, "set_birthdate", CitizenData.BIRTHDATE),
    (CitizenPage, "fill_data", CitizenPage.DATA),
    (DataPage, "fill_reg_data", DataPage.REG_DATA),
    (DataPage, "fill_birth_date", DataPage.BIRTH_DATE),
])
def test_all_selenium_date_fields_use_shared_helper(cls, method, locator):
    page = cls(page_mock(WebDriver))
    with patch.object(page, "fill_date", autospec=True) as fill:
        getattr(page, method)("02.01.1990")
    fill.assert_called_once_with(locator, "02.01.1990")


def test_user_checks_use_real_page_interface():
    page = page_mock(UserPage)
    page.required_values.return_value = ["", ""]
    page.next_is_enabled.return_value = False
    page.is_open.return_value = False
    user.check_required_fields_empty(page, 2)
    user.check_next_button_enabled(page, False)
    user.check_user_form_closed(page)
    page.required_values.return_value = ["filled", ""]
    with pytest.raises(AssertionError, match="not empty"):
        user.check_required_fields_empty(page, 2)


def test_user_page_reads_actual_elements_and_waits_for_close():
    driver = page_mock(WebDriver)
    field = page_mock(WebElement)
    field.is_displayed.return_value = True
    field.is_enabled.return_value = False
    field.get_property.return_value = ""
    driver.find_element.return_value = field
    driver.find_elements.return_value = [field, field]
    page = UserPage(driver)
    assert page.required_values() == ["", ""]
    assert page.next_is_enabled() is False
    assert page.is_open() is True
    field.is_enabled.return_value = True
    field.click.side_effect = lambda: setattr(field.is_displayed, "return_value", False)
    with patch.object(page.wait, "until", wraps=page.wait.until) as waited:
        page.close()
    assert waited.call_count == 2  # Clickability, then dialog invisibility.
    assert driver.find_element.call_args == call(*UserPage.TITLE)
    assert page.is_open() is False


@pytest.mark.parametrize("new_surname", [None, "", "Учебная"])
def test_service_data_uses_existing_spouse_setters(new_surname):
    page = page_mock(DataPage)
    data.fill_service_data(
        page, "2026-01-01", "Фамилия", "Имя", "Отчество", "1991-02-03", "TS123456",
        new_surname=new_surname,
    )
    expected = [call.fill_reg_data("2026-01-01")]
    if new_surname is not None:
        expected.append(call.fill_new_surname(new_surname))
    expected += [call.fill_surname_sup("Фамилия"), call.fill_name_sup("Имя"),
                 call.fill_lastname_sup("Отчество"), call.fill_birth_date("1991-02-03"),
                 call.fill_pasport("TS123456")]
    assert page.mock_calls == expected


def test_explicit_names_preserve_legacy_setter_mapping():
    page = page_mock(CitizenData)
    citizen.fill_citizen_family_name(page, "Фамилия")
    citizen.fill_citizen_patronymic(page, "Отчество")
    assert page.mock_calls == [call.set_lastname("Фамилия"), call.set_surname("Отчество")]
    actual = CitizenData(page_mock(WebDriver))
    with patch.object(actual, "visible") as visible:
        field = visible.return_value
        field.get_property.return_value = "Отчество"
        actual.driver.find_element.return_value = field
        actual.set_surname("Отчество")
        visible.assert_called_with(CitizenData.SURNAME)
        assert "Отчество" in CitizenData.SURNAME[1]
        field.get_property.return_value = "Фамилия"
        actual.set_lastname("Фамилия")
        visible.assert_called_with(CitizenData.LASTNAME)
        assert "Фамилия" in CitizenData.LASTNAME[1]


@pytest.mark.parametrize("cls,step,result_cls,target", [
    (UserPage, user.open_service_choice, Application_choice, Application_choice.BUTTON),
    (Application_choice, user.open_wedding_citizen_form, CitizenPage, CitizenPage.TITLE),
    (Application_choice, citizen.open_app_citizen_form, CitizenData, CitizenData.BIRTHDATE),
    (CitizenData, app.open_app_data_form, AppData, AppData.BIRTHPLACE),
    (CitizenData, citizen.next_to_applicationdata, AppData, AppData.BIRTHPLACE),
    (CitizenPage, citizen.click_next_on_citizen, DataPage, DataPage.TITLE),
    (DataPage, data.click_finish, StatusPage, StatusPage.TITLE),
    (AppData, app.next_to_applicationstatus, AppStatuspage, AppStatuspage.TITLE),
])
def test_transitions_return_ready_pages_with_same_driver_and_timeout(cls, step, result_cls, target):
    driver = page_mock(WebDriver)
    element = page_mock(WebElement)
    element.is_displayed.return_value = True
    element.is_enabled.return_value = True
    driver.find_element.return_value = element
    result = step(cls(driver, timeout=7))
    assert isinstance(result, result_cls)
    assert result.driver is driver
    assert result.timeout == 7
    element.click.assert_called_once_with()
    assert driver.find_element.call_args == call(*target)


@pytest.mark.parametrize("filename,birth", [
    ("roman/test_registration_birth.py", True),
    ("daniil/test_registration_wedding.py", False),
])
def test_registration_flows_use_actual_interfaces_and_safe_synthetic_data(filename, birth):
    module = runpy.run_path(str(Path(__file__).parents[1] / filename))
    assert {mark.name for mark in module["pytestmark"]} == {"ui", "defense_write"}
    home, applicant = page_mock(HomePage), page_mock(UserPage)
    home.open_user.return_value = applicant
    person = page_mock(CitizenData if birth else CitizenPage)
    service = page_mock(AppData if birth else DataPage)
    status = page_mock(AppStatuspage if birth else StatusPage)
    status.get_application_number.return_value = "123"
    status.get_status.return_value = "На рассмотрении."
    choice = page_mock(Application_choice)
    applicant.click_next.return_value = choice
    if birth:
        choice.birthapp_choice.return_value = person
        person.next.return_value = service
        service.finish.return_value = status
    else:
        choice.wedding_choice.return_value = person
        person.click_next.return_value = service
        service.click_finish.return_value = status
    flow = module["test_open_user_form_and_fill_surname"]
    with patch.dict(flow.__globals__, open_zags=lambda driver, settings: home):
        flow(object(), object())
        first_passport = applicant.fill_pasport.call_args.args[0]
        flow(object(), object())
    second_passport = applicant.fill_pasport.call_args.args[0]
    assert first_passport != second_passport
    passport = person.set_passport if birth else person.fill_pasport
    values = [first_passport, second_passport, passport.call_args.args[0]]
    if not birth:
        values.append(service.fill_pasport.call_args.args[0])
        service.fill_birth_date.assert_called_with("1991-01-01")
        service.fill_reg_data.assert_called_with("2026-01-01")
        service.fill_new_surname.assert_called_with("Учебная")
    else:
        person.set_lastname.assert_called_with("Учебный")
        person.set_surname.assert_called_with("Тестович")
        person.set_birthdate.assert_called_with("2026-01-01")
    assert all(value.startswith("T") and len(value) == 8 for value in values)
    assert len(values) == len(set(values))
    assert status.get_status.call_count == 2


@pytest.mark.parametrize("surname", [None, "Training", "Учебный"])
def test_user_smoke_flows_use_real_interfaces_without_submission(surname):
    module = runpy.run_path(str(Path(__file__).parents[1] / "ui" / "test_user_smoke.py"))
    assert {mark.name for mark in module["pytestmark"]} == {"ui", "smoke"}
    home, page = page_mock(HomePage), page_mock(UserPage)
    home.open_user.return_value = page
    page.required_values.return_value = [""] * 6
    page.next_is_enabled.return_value = False
    page.is_open.return_value = False
    page.fill_surname.side_effect = lambda value: setattr(page.surname_value, "return_value", value)
    name = ("test_empty_user_form_disables_next" if surname is None
            else "test_user_surname_can_be_entered_and_cleared")
    flow = module[name]
    args = () if surname is None else (surname,)
    with patch.dict(flow.__globals__, open_zags=lambda driver, settings: home):
        flow(object(), object(), *args)
    page.close.assert_called_once_with()
    page.is_open.assert_called_once_with()
    page.click_next.assert_not_called()
    page.click_brak.assert_not_called()
    if surname is not None:
        assert page.fill_surname.call_args_list == [call(surname), call("")]
