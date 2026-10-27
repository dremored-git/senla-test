import allure
import pytest

from zags.steps.admin import (
    check_admin_form_closed,
    check_admin_surname,
    check_next_button_enabled,
    check_required_fields_empty,
    close_admin_form,
    fill_admin_surname,
    open_admin_form,
)
from zags.steps.navigation import open_zags

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@allure.epic("ЗАГС")
@allure.feature("Администратор")
@allure.story("Обязательные поля")
@allure.title("Пустая форма администратора: кнопка Далее недоступна")
def test_empty_admin_form_disables_next(driver, settings):
    home = open_zags(driver, settings)
    admin = open_admin_form(home)
    check_required_fields_empty(admin, expected_count=6)
    check_next_button_enabled(admin, expected=False)
    close_admin_form(admin)
    check_admin_form_closed(admin)


@allure.epic("ЗАГС")
@allure.feature("Администратор")
@allure.story("Ввод и очистка фамилии")
@allure.title("Ввод и очистка фамилии: {param_id}")
@pytest.mark.parametrize("surname", ["Training", "Иванов"], ids=["latin", "cyrillic"])
def test_surname_can_be_entered_and_cleared(driver, settings, surname):
    home = open_zags(driver, settings)
    admin = open_admin_form(home)
    fill_admin_surname(admin, value=surname)
    check_admin_surname(admin, expected=surname)
    fill_admin_surname(admin, value="")
    check_admin_surname(admin, expected="")
    check_next_button_enabled(admin, expected=False)
    close_admin_form(admin)
    check_admin_form_closed(admin)
