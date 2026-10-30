"""Importable API actions and assertions used by tests and fixtures."""
import allure
import pytest
from requests import Response

from zags.api.client import ZagsApi


@allure.step("Получить список заявок")
def get_applications(api: ZagsApi, limit: int = 2, offset: int = 0) -> Response:
    return api.get_applications(limit=limit, offset=offset)


@allure.step("Проверка, что список заявок не превышает указанный лимит")
def get_applications_length_limit(api:ZagsApi, body:dict, limit: int = 2, offset: int = 0) -> list[dict]:
    length=body["data"]
    assert len(length)<=limit, f"Expected data limit{limit}, got len(data)={len(length)}"
    return api.get_applications(limit=limit, offset=offset)


@allure.step("Получить статус заявки {application_id}")
def get_application_status(api: ZagsApi, application_id: int) -> Response:
    return api.get_application_status(application_id)


@allure.step("Создать администратора с синтетическими данными")
def create_admin(api: ZagsApi, payload: dict) -> Response:
    return api.create_admin(payload)


@allure.step("Проверить HTTP-статус: {expected}")
def check_status_code(response: Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"HTTP status: expected {expected}, got {response.status_code}; "
        f"Content-Type={response.headers.get('Content-Type', '')!r}"
    )


@allure.step("Прочитать JSON-объект ответа")
def read_json_object(response: Response) -> dict:
    content_type = response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
    assert content_type == "application/json", f"Expected JSON, got Content-Type={content_type!r}"
    try:
        body = response.json()
    except ValueError as error:
        raise AssertionError("Response is not valid JSON") from error
    assert isinstance(body, dict), f"Expected JSON object, got {type(body).__name__}"
    return body


@allure.step("Проверить список заявок")
def check_applications_body(body: dict) -> list[dict]:
    assert "data" in body, "Response has no data field"
    data=body["data"]
    if data is None or data == {}:
        pytest.skip("Response 'data' пустая — проверять нечего (на стенде нет заявки)")
    rows = body["data"]
    assert isinstance(rows, list), "data must be a list"
    for index, row in enumerate(rows):
        assert isinstance(row, dict), f"data[{index}] must be an object"
        identifier = row.get("applicationid")
        assert type(identifier) is int and identifier > 0, (
            f"data[{index}].applicationid must be a positive integer, got {identifier!r}"
        )
    return rows


@allure.step("Проверить корректность ID в списке заявок")
def check_app_id_is_correct(body: dict) -> list[dict]:
    assert "data" in body, "Response has no data field"
    rows=body["data"]
    for i in (rows):
        correctid=i["applicationid"]
        assert isinstance (correctid,dict), (f"data [{i}] does not exist!")
    return rows


@allure.step("Проверить поля статуса заявки")
def check_application_status_body(body: dict) -> dict:
    data = body.get("data")
    assert isinstance(data, dict), "data must be an application status object"
    required = {"dateofapplication", "kindofapplication", "statusofapplication"}
    assert required <= data.keys(), f"Missing fields: {sorted(required - data.keys())}"
    for key in sorted(required):
        assert isinstance(data[key], str) and data[key].strip(), f"{key} must be a non-empty string"
    return data


@allure.step ("Проверить совпадение статуса заявки")
def check_application_kindofstatus(body: dict) -> dict:
    data=body.get("kindofapplication[0]")
    assert data=="kindofapplication[0]", f"{data}is not correct!"


@allure.step("Проверить ID созданного администратора")
def check_created_admin(body: dict) -> int:
    identifier = body.get("staffid")
    assert type(identifier) is int and identifier > 0, (
        f"Expected positive staffid according to Swagger, got {identifier!r}"
    )
    return identifier
