import json

import allure
import pytest

from zags.steps.api import (
    check_application_status_body,
    check_applications_body,
    check_status_code,
    get_application_status,
    get_applications,
    read_json_object,
)

pytestmark = [pytest.mark.api, pytest.mark.smoke]


@allure.parent_suite("API")
@allure.suite("Заявки и авторизация")
@allure.link("https://regoffice.senla.eu/swagger/", name="Swagger ЗАГСа")
@allure.epic("ЗАГС")
@allure.feature("API заявок")
@allure.story("Чтение заявок")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "Получаем список заявок. Проверяем HTTP 200, JSON и ID записей. "
    "Обертка data основана на сверке стенда; Swagger описывает ее неполно."
)
@allure.title("GET /getApplications: доступен список заявок")
def test_get_applications_returns_list(api_client):
    response = get_applications(api_client, limit=2, offset=0)
    with allure.step("Проверить успешный ответ списка заявок"):
        check_status_code(response, expected=200)
        body = read_json_object(response)
        rows = check_applications_body(body)
    allure.attach(
        json.dumps(
            {"returned_count": len(rows), "response_fields": sorted(body)},
            ensure_ascii=False,
            indent=2,
        ),
        name="Сводка ответа без персональных данных",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.parent_suite("API")
@allure.suite("Заявки и авторизация")
@allure.link("https://regoffice.senla.eu/swagger/", name="Swagger ЗАГСа")
@allure.epic("ЗАГС")
@allure.feature("API заявок")
@allure.story("Статус существующей заявки")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "ID получаем из списка в фикстуре. Не создаем запись и не фиксируем "
    "конкретный статус общей заявки. Проверяем структуру фактического ответа."
)
@allure.title("GET /getApplStatus: статус существующей заявки")
def test_get_existing_application_status(api_client, existing_application_id):
    allure.dynamic.title(f"GET /getApplStatus: заявка {existing_application_id}")
    allure.dynamic.parameter("application_id", existing_application_id)
    response = get_application_status(api_client, existing_application_id)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_application_status_body(body)


@allure.parent_suite("API")
@allure.suite("Заявки и авторизация")
@allure.link("https://regoffice.senla.eu/swagger/", name="Swagger ЗАГСа")
@allure.epic("ЗАГС")
@allure.feature("HTTP Basic Auth")
@allure.story("Отказ без корректной авторизации")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "Два варианта одной проверки: отсутствующий Basic Auth и неверные доступы. "
    "Ожидаем 401 по сверке стенда. HTML-тело отказа не декодируем как JSON."
)
@allure.title("GET /getApplications: отказ в доступе ({param_id})")
def test_get_applications_requires_auth(unauthorized_api_client):
    response = get_applications(unauthorized_api_client)
    check_status_code(response, expected=401)
