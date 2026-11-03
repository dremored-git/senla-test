from unittest.mock import call, create_autospec

import pytest

from zags.pages.application_choice import Application_choice
from zags.pages.Citizen_data import CitizenData
from zags.pages.citizen_page import CitizenPage
from zags.steps import citizen


@pytest.mark.parametrize(
    "step,method,args",
    [
        (citizen.fill_citizen_surname, "set_surname", ("Training",)),
        (citizen.fill_citizen_firstname, "set_firstname", ("Test",)),
        (citizen.fill_citizen_lastname, "set_lastname", ("Tester",)),
        (citizen.fill_citizen_birthdate, "set_birthdate", ("1990-01-01",)),
        (citizen.fill_citizen_passport, "set_passport", ("TEST1234",)),
        (citizen.fill_citizen_gender, "set_gender", ("муж",)),
        (citizen.fill_user_adress, "set_adress", ("Test address",)),
        (citizen.next_to_applicationdata, "next", ()),
        (citizen.close_citizen_form, "close", ()),
    ],
)
def test_roman_steps_keep_existing_page_interface(step, method, args):
    page = create_autospec(CitizenData, instance=True, spec_set=True)
    step(page, *args)
    getattr(page, method).assert_called_once_with(*args)


def test_open_citizen_form_keeps_service_choice_result():
    choice = create_autospec(Application_choice, instance=True, spec_set=True)
    assert citizen.open_app_citizen_form(choice) is choice.birthapp_choice.return_value
    choice.birthapp_choice.assert_called_once_with()


def test_daniil_fill_uses_actual_page_methods_in_order():
    page = create_autospec(CitizenPage, instance=True, spec_set=True)
    citizen.fill_citizen_data(page, birth_date="1990-01-01", address="Test address")
    citizen.click_next_on_citizen(page)
    assert page.mock_calls == [
        call.fill_data("1990-01-01"),
        call.fill_address("Test address"),
        call.click_next(),
    ]


@pytest.mark.parametrize(
    "step,method,value,args,error",
    [
        (citizen.check_required_fields_filled, "required_values", ["filled", ""], (2,), "empty"),
        (
            citizen.check_required_fields_filled,
            "required_values",
            ["filled"],
            (2,),
            "Required fields",
        ),
        (citizen.check_next_button_enabled, "next_is_enabled", False, (True,), "Next button"),
        (citizen.check_citizen_form_closed, "is_open", True, (), "still open"),
    ],
)
def test_merged_checks_still_reject_wrong_state(step, method, value, args, error):
    page = create_autospec(CitizenData, instance=True, spec_set=True)
    getattr(page, method).return_value = value
    with pytest.raises(AssertionError, match=error):
        step(page, *args)
