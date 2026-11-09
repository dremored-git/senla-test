import allure
import pytest

from zags.steps.api import (
    check_app_id_is_correct,
    check_application_kindofstatus,
    check_applications_body,
    check_status_code,
    get_application_status,
    get_applications,
    get_applications_length_limit,
    read_json_object,
)

pytestmark = [
    pytest.mark.api,
    pytest.mark.smoke,
    allure.epic("ЗАГС"),
    allure.feature("API: Роман"),
]


@allure.title("Список заявок с лимитом {limit} содержит корректные ID")
@pytest.mark.parametrize("limit", [1, 3], ids=["one", "three"])
def test_get_applications_limit(api_client, limit):
    response = get_applications(api_client, limit=limit)
    check_status_code(response, expected=200)
    check_applications_body(read_json_object(response))


@allure.title("Число заявок не превышает лимит {limit}")
@pytest.mark.parametrize("limit", [1, 3], ids=["one", "three"])
def test_get_applications_limit_list(api_client, limit):
    response = get_applications(api_client, limit=limit)
    check_status_code(response, expected=200)
    body = read_json_object(response)
    rows = get_applications_length_limit(api_client, body, limit=limit)
    allure.attach(str(len(rows)), "Returned row count", allure.attachment_type.TEXT)


@allure.title("Все ID в списке — положительные целые числа")
def test_get_existing_application_status(api_client):
    response = get_applications(api_client, limit=10)
    check_status_code(response, expected=200)
    check_app_id_is_correct(read_json_object(response))


@allure.title("Вид заявки из списка совпадает с видом в ее статусе")
def test_get_existing_application_status_by_id(api_client):
    response = get_applications(api_client, limit=1)
    check_status_code(response, expected=200)
    rows = check_applications_body(read_json_object(response))
    if not rows:
        pytest.skip("No existing application for a read-only comparison")
    source = rows[0]
    identifier = source["applicationid"]
    allure.dynamic.parameter("application_id", identifier)
    details = get_application_status(api_client, identifier)
    check_status_code(details, expected=200)
    check_application_kindofstatus(
        read_json_object(details), expected=source["kindofapplication"]
    )
