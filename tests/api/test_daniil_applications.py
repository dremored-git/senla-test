import allure
import pytest

from zags.steps.api import (
    get_application_status,
    get_applications,
    check_status_code,
    read_json_object,
    check_applications_body,
    check_application_status_body,
)

pytestmark = [pytest.mark.api]

@allure.feature("Заявки")
@allure.story("Пагинация")
@allure.title("Проверка пагинации limit={limit}")
@pytest.mark.parametrize("limit", [1, 3], ids=["limit_1", "limit_3"])

def test_pagination(api_client, limit):
    response = get_applications(api_client, limit=limit, offset=0)  # <-- добавили response =
    check_status_code(response, expected=200)
    body = read_json_object(response)
    rows = check_applications_body(body)
    assert len(rows) <= limit


@allure.feature("Заявки")
@allure.story("Чтение одной заявки")
@allure.title("Сверка kindofapplication из списка и карточки")
def test_single_application(api_client):
    response_list = get_applications(api_client, limit=10, offset=0)
    check_status_code(response_list, expected=200)
    body_list = read_json_object(response_list)
    rows = check_applications_body(body_list)
    
    if not rows:
        pytest.skip("Список заявок пуст, нечего проверять")
   
    first_app = rows[0]
    app_id = first_app["applicationid"]
    kind_from_list = first_app["kindofapplication"]
   
    response_single = get_application_status(api_client, application_id=app_id)
    check_status_code(response_single, expected=200)
    
    body_single = read_json_object(response_single)
    status_data = check_application_status_body(body_single)
    kind_from_single = status_data["kindofapplication"]

    assert kind_from_single == kind_from_list, (
        f"kindofapplication не совпадает: в списке {kind_from_list}, в карточке {kind_from_single}"
    )