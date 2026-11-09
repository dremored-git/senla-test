from uuid import uuid4

import allure
import pytest

expect = pytest.importorskip("playwright.sync_api").expect

from zags.defense.playwright_steps import (  # noqa: E402 - optional dependency checked above
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
    allure.feature("Playwright: Даниил"),
]


@allure.title("Пустая форма пользователя блокирует переход")
def test_daniil_empty_form(defense_page, settings):
    form = open_registration(defense_page, settings)
    expect(form.button("Далее")).to_be_disabled()
    form.button("Закрыть").click()
    expect(form.dialog).not_to_be_visible()


@pytest.mark.defense_write
@allure.title("Полная регистрация: Регистрация брака")
def test_daniil_registration(defense_page, settings, defense_log):
    form = open_registration(defense_page, settings)
    fill_applicant(form, passport="T" + uuid4().hex[:7])
    choose_service(form, service="Регистрация брака")
    fill_citizen(form)
    fill_service(form, service="wedding")
    identifier = submit_registration(form)
    allure.dynamic.parameter("created_application_id", identifier)
    defense_log.info("Playwright registration checked: application_id=%s", identifier)


@allure.title("Все этапы формы подготовлены без отправки")
def test_daniil_prepare_without_submit(defense_page, settings):
    form = open_registration(defense_page, settings)
    fill_applicant(form, passport="T" + uuid4().hex[:7])
    choose_service(form, service="Регистрация брака")
    fill_citizen(form)
    fill_service(form, service="wedding")
    expect(form.button("Завершить")).to_be_enabled()
    form.button("Закрыть").click()
    expect(form.dialog).not_to_be_visible()
