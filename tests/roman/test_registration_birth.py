from uuid import uuid4

import allure
import pytest

from zags.steps.app import (
    fill_app_birthblase,
    fill_app_father,
    fill_app_grandfather,
    fill_app_grandmother,
    fill_app_mother,
    next_to_applicationstatus,
    open_app_data_form,
)
from zags.steps.checkstatus import check_application_number_not_empty, check_application_status
from zags.steps.citizen import (
    fill_citizen_birthdate,
    fill_citizen_family_name,
    fill_citizen_firstname,
    fill_citizen_gender,
    fill_citizen_passport,
    fill_citizen_patronymic,
    fill_user_adress,
    open_app_citizen_form,
)
from zags.steps.navigation import open_zags
from zags.steps.user import fill_user_data, open_service_choice, open_user_form

pytestmark = [pytest.mark.ui, pytest.mark.defense_write]


@allure.epic("ЗАГС")
@allure.feature("Пользователь")
@allure.story("Заявка на регистрацию услуги 'Регистрация рождения'")
@allure.title("Все этапы регистрации заявки: от данных пользователя до статуса заявки")
def test_open_user_form_and_fill_surname(driver, settings):
    home = open_zags(driver, settings)
    user = open_user_form(home)
    fill_user_data(
        user, family_name="Учебный", name="Тест", patronymic="Тестович",
        phone="00000000000", passport="T" + uuid4().hex[:7], address="Учебный адрес 1",
    )
    choice = open_service_choice(user)
    citizen = open_app_citizen_form(choice)
    fill_citizen_family_name(citizen, "Учебный")
    fill_citizen_firstname(citizen, "Тест")
    fill_citizen_patronymic(citizen, "Тестович")
    fill_citizen_birthdate(citizen, "2026-01-01")
    fill_citizen_passport(citizen, "T" + uuid4().hex[:7])
    fill_citizen_gender(citizen, "муж")
    fill_user_adress(citizen, "Учебный адрес 1")
    data = open_app_data_form(citizen)
    fill_app_birthblase(data, "Учебный город")
    fill_app_mother(data, "Тестовая мать")
    fill_app_father(data, "Тестовый отец")
    fill_app_grandmother(data, "Тестовая бабушка")
    fill_app_grandfather(data, "Тестовый дедушка")
    status = next_to_applicationstatus(data)
    check_application_number_not_empty(status)
    check_application_status(status, expected_status="На рассмотрении.")
