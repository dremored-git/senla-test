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

pytestmark = [
    pytest.mark.defense_live,
    allure.epic("ЗАГС"),
    allure.feature("API: Роман"),
    allure.link("https://regoffice.senla.eu/swagger/", name="Swagger"),
]


@allure.title("Список заявок: ограничение размера страницы {param_id}")
@allure.story("Чтение заявок")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Лимит — согласованное наблюдаемое поведение стенда; без POST.")
@pytest.mark.parametrize("limit", [1, 3], ids=["one", "three"])
def test_roman_list_limit(defense_api, defense_log, limit):
    response = get_applications(defense_api, limit=limit)
    defense_log.info("list completed: HTTP %s", response.status_code)
    check_status_code(response, expected=200)
    rows = check_applications_body(read_json_object(response))
    with allure.step("Проверить максимальное число строк"):
        assert len(rows) <= limit, f"Expected at most {limit} rows, got {len(rows)}"
    allure.attach(
        json.dumps({"returned": len(rows), "limit": limit}),
        name="Response summary",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.title("Вид заявки совпадает в списке и деталях")
@allure.story("Связанная проверка двух эндпоинтов")
def test_roman_list_matches_details(defense_api, defense_log):
    response = get_applications(defense_api, limit=1)
    check_status_code(response, expected=200)
    rows = check_applications_body(read_json_object(response))
    if not rows:
        pytest.skip("No records: read-only scenario cannot select an existing ID")
    identifier = rows[0]["applicationid"]
    allure.dynamic.parameter("application_id", identifier)
    details = get_application_status(defense_api, identifier)
    check_status_code(details, expected=200)
    data = check_application_status_body(read_json_object(details))
    assert data["kindofapplication"] == rows[0]["kindofapplication"]
    defense_log.info("list/detail relationship checked")
