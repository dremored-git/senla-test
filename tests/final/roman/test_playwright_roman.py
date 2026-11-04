from uuid import uuid4

import allure
import pytest
from playwright.sync_api import expect

from zags.defense.playwright_steps import (
    choose_service,
    fill_applicant,
    fill_citizen,
    fill_service,
    open_registration,
    submit_registration,
)

pytestmark = [
    pytest.mark.defense_live,
    pytest.mark.defense_pw,
    allure.epic("ЗАГС"),
    allure.feature("Playwright: Роман"),
]


@allure.title("Пустая форма пользователя блокирует переход")
def test_roman_empty_form(defense_page, settings):
    form = open_registration(defense_page, settings)
    expect(form.button("Далее")).to_be_disabled()
    form.button("Закрыть").click()
    expect(form.dialog).not_to_be_visible()


@pytest.mark.defense_write
@allure.title("Полная регистрация: Регистрация рождения")
def test_roman_registration(defense_page, settings, defense_log):
    form = open_registration(defense_page, settings)
    fill_applicant(form, passport="T" + uuid4().hex[:7])
    choose_service(form, service="Регистрация рождения")
    fill_citizen(form)
    fill_service(form, service="birth")
    identifier = submit_registration(form)
    allure.dynamic.parameter("created_application_id", identifier)
    defense_log.info("Playwright registration checked: application_id=%s", identifier)


@allure.title("Все этапы формы подготовлены без отправки")
def test_roman_prepare_without_submit(defense_page, settings):
    form = open_registration(defense_page, settings)
    fill_applicant(form, passport="T" + uuid4().hex[:7])
    choose_service(form, service="Регистрация рождения")
    fill_citizen(form)
    fill_service(form, service="birth")
    expect(form.button("Завершить")).to_be_enabled()
    form.button("Закрыть").click()
    expect(form.dialog).not_to_be_visible()
