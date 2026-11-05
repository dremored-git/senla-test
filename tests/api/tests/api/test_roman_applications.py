import json

import allure
import pytest

from zags.steps.api import (
    check_app_id_is_correct,
    check_application_kindofstatus,
    check_application_status_body,
    check_applications_body,
    check_status_code,
    get_application_status,
    get_applications,
    get_applications_length_limit,
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
@allure.title("GET /getApplications: доступен список заявок c ограничением показа 1 и 3")
@pytest.mark.parametrize("limit", [1, 3], ids=["Limit 1", "Limit 3"])
def test_get_applications_limit(api_client, limit):
    response = get_applications(api_client, limit, offset=0)
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
@allure.story("Чтение заявок")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "Получаем список заявок. Проверяем HTTP 200, JSON и ID записей. "
    "Обертка data основана на сверке стенда; Swagger описывает ее неполно."
)
@allure.title("GET /getApplications: корректное отображение списка заявок с указанным лимитом")
@pytest.mark.parametrize("limit", [1, 3], ids=["Limit 1", "Limit 3"])
def test_get_applications_limit_list(api_client, limit):
    response = get_applications(api_client, limit, offset=0)
    with allure.step("Проверить успешный ответ списка заявок"):
        check_status_code(response, expected=200)
        body = read_json_object(response)
        rows = check_applications_body(body)
    with allure.step("Проверить корректное отображение списка заявок с указанным лимитом"):
        rows = get_applications_length_limit(api_client,limit=limit,offset=0,body=body,)
        return rows
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
@allure.title("GET /getApplications: корректность существующих заявок")
def test_get_existing_application_status(api_client, existing_applications_id):
    allure.dynamic.title(f"GET /getApplStatus: заявка {existing_applications_id}")
    allure.dynamic.parameter("application_id", existing_applications_id)
    response = get_application_status(api_client, existing_applications_id)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_app_id_is_correct(body)


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
@allure.title("GET /getApplStatus: чтение существующей заявки и ее статуса по id")
def test_get_existing_application_status_by_id(api_client, existing_application_id_test_roman):
    body=get_applications(api_client, limit=10, offset=0)
    position=read_json_object(body)
    k=position[0]["applicationid"]
    firstone=k[0]
    firstappl=firstone["applicationid"]
    existing_application_id=firstappl["applicationid"]
    allure.dynamic.title(f"GET /getApplStatus: заявка {existing_application_id_test_roman}")
    allure.dynamic.parameter("application_id", existing_application_id_test_roman)
    response = get_application_status(api_client, body)
    body=read_json_object(response)
    rows=body["kindofapplication"]
    first=rows[0]
    applicationstatus=first["kindofapplication"]
    check_application_kindofstatus(applicationstatus, expected=applicationstatus)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_application_status_body(body)