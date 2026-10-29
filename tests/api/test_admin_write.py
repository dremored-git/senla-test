import allure
import pytest

from zags.api.data import make_admin_payload
from zags.steps.api import check_created_admin, check_status_code, create_admin, read_json_object

pytestmark = [pytest.mark.api, pytest.mark.api_write]


@allure.epic("ЗАГС")
@allure.feature("API администратора")
@allure.story("Создание синтетической записи")
@allure.title("POST /sendAdminRequest: создать администратора")
def test_create_admin_returns_id(api_client):
    payload = make_admin_payload()
    response = create_admin(api_client, payload)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    check_created_admin(body)
