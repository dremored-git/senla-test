import allure
import pytest

from zags.steps.navigation import open_zags
from zags.steps.user import (
    check_next_button_enabled,
    check_required_fields_empty,
    check_user_form_closed,
    check_user_surname,
    close_user_form,
    fill_user_surname,
    open_user_form,
)

pytestmark = [pytest.mark.ui, pytest.mark.smoke]


@allure.epic("ЗАГС")
@allure.feature("Пользователь")
@allure.story("Обязательные поля")
@allure.title("Пустая форма пользователя: кнопка Далее недоступна")
def test_empty_user_form_disables_next(driver, settings):
    home = open_zags(driver, settings)
    user = open_user_form(home)
    check_required_fields_empty(user, expected_count=6)
    check_next_button_enabled(user, expected=False)
    close_user_form(user)
    check_user_form_closed(user)


@allure.epic("ЗАГС")
@allure.feature("Пользователь")
@allure.story("Ввод и очистка фамилии")
@allure.title("Ввод и очистка фамилии пользователя: {param_id}")
@pytest.mark.parametrize("surname", ["Training", "Учебный"], ids=["latin", "cyrillic"])
def test_user_surname_can_be_entered_and_cleared(driver, settings, surname):
    home = open_zags(driver, settings)
    user = open_user_form(home)
    fill_user_surname(user, value=surname)
    check_user_surname(user, expected=surname)
    fill_user_surname(user, value="")
    check_user_surname(user, expected="")
    check_next_button_enabled(user, expected=False)
    close_user_form(user)
    check_user_form_closed(user)
