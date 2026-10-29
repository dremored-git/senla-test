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


@allure.epic("ЗАГС")
@allure.feature("API заявок")
@allure.story("Чтение заявок")
@allure.title("GET /getApplications: доступен список заявок")
def test_get_applications_returns_list(api_client):
    response = get_applications(api_client, limit=2, offset=0)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_applications_body(body)


@allure.epic("ЗАГС")
@allure.feature("API заявок")
@allure.story("Статус существующей заявки")
@allure.title("GET /getApplStatus: статус существующей заявки")
def test_get_existing_application_status(api_client, existing_application_id):
    response = get_application_status(api_client, existing_application_id)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_application_status_body(body)


@allure.epic("ЗАГС")
@allure.feature("HTTP Basic Auth")
@allure.story("Отказ без корректной авторизации")
@allure.title("GET /getApplications: отказ в доступе ({param_id})")
def test_get_applications_requires_auth(unauthorized_api_client):
    response = get_applications(unauthorized_api_client)
    check_status_code(response, expected=401)
