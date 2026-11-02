import logging
from uuid import uuid4

import allure

from zags.api.client import ZagsApi
from zags.steps.api import check_status_code, read_json_object

LOG = logging.getLogger(__name__)


class RegistrationApi(ZagsApi):
    def create_client(self, payload):
        return self._request("POST", "/sendUserRequest", json=payload, headers={"Channel": "web"})


def client_payload(owner):
    suffix = uuid4().hex[:7]
    return {
        "mode": "birth",
        "personalLastName": "Учебный" + owner,
        "personalFirstName": "Тест",
        "personalMiddleName": "Тестович",
        "personalPhoneNumber": "00000000000",
        "personalNumberOfPassport": "T" + suffix,
        "personalAddress": "Учебный адрес 1",
        "citizenLastName": "Учебный",
        "citizenFirstName": "Ребенок",
        "citizenMiddleName": "Тестович",
        "citizenBirthDate": "2020-01-01",
        "citizenNumberOfPassport": "",
        "citizenGender": "муж",
        "citizenAddress": "Учебный адрес 1",
        "birth_place": "Учебный город",
        "birth_mother": "Тестовая мать",
        "birth_father": "Тестовый отец",
        "birth_grandma": "Тестовая бабушка",
        "birth_grandpa": "Тестовый дедушка",
    }


def admin_payload(owner):
    from zags.api.data import make_admin_payload

    return make_admin_payload(
        personalLastName="Учебный" + owner, personalNumberOfPassport="T" + uuid4().hex[:7]
    )


@allure.step("Создать клиента и получить ID")
def create_client(api, payload):
    response = api.create_client(payload)
    LOG.info("create_client completed: HTTP %s", response.status_code)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    return created_id(body, "applicantid"), created_id(body, "applicationid")


@allure.step("Создать администратора и получить ID")
def create_admin(api, payload):
    response = api.create_admin(payload)
    LOG.info("create_admin completed: HTTP %s", response.status_code)
    check_status_code(response, expected=200)
    return created_id(read_json_object(response), "staffid")


def created_id(body, key):
    data = body.get("data")
    assert isinstance(data, dict), "Expected response.data object; inspect API contract"
    value = data.get(key)
    assert type(value) is int and value > 0, f"Expected positive data.{key}, got {value!r}"
    return value


@allure.step("Сравнить сохраненную запись с отправленными данными")
def check_person(row, payload):
    assert row is not None, "Created record not found by its returned ID"
    fields = {
        "surname": "personalLastName",
        "name": "personalFirstName",
        "middlename": "personalMiddleName",
        "passportnumber": "personalNumberOfPassport",
    }
    for column, key in fields.items():
        assert row[column] == payload[key], f"Mismatch in saved {column}"
