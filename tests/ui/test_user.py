from uuid import uuid4

import allure
import pytest

from zags.steps.citizen import click_next_on_citizen, fill_wedding_citizen_data
from zags.steps.data import click_finish, fill_service_data
from zags.steps.navigation import open_zags
from zags.steps.status import check_application_number_not_empty, check_application_status
from zags.steps.user import (
    fill_user_data,
    open_service_choice,
    open_user_form,
    open_wedding_citizen_form,
)

pytestmark = [pytest.mark.ui, pytest.mark.defense_write]


@allure.feature("Регистрация заявки")
@allure.story("Успешная регистрация брака")
@allure.title("Проверка сквозной регистрации заявки")
def test_open_user_form_and_fill_surname(driver, settings):
    home = open_zags(driver, settings)
    user = open_user_form(home)
    fill_user_data(
        user, family_name="Учебный", name="Тест", patronymic="Тестович",
        phone="00000000000", passport="T" + uuid4().hex[:7], address="Учебный адрес 1",
    )
    choice = open_service_choice(user)
    citizen = open_wedding_citizen_form(choice)
    fill_wedding_citizen_data(
        citizen, family_name="Учебный", name="Тест", patronymic="Тестович",
        birth_date="1990-01-01", passport="T" + uuid4().hex[:7],
        gender="муж", address="Учебный адрес 1",
    )
    data = click_next_on_citizen(citizen)
    fill_service_data(
        data, reg_date="2026-01-01", new_surname="Учебная",
        spouse_surname="Учебная", spouse_name="Тест", spouse_patronymic="Тестовна",
        spouse_birth_date="1991-01-01", spouse_passport="T" + uuid4().hex[:7],
    )
    status = click_finish(data)
    check_application_number_not_empty(status)
    check_application_status(status, expected_status="На рассмотрении.")
