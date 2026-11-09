import allure
import pytest

from zags.defense.api_steps import (
    admin_payload,
    check_person,
    client_payload,
    create_admin,
    create_client,
)
from zags.steps.api import check_applications_body, check_status_code, read_json_object

pytestmark = [
    pytest.mark.defense_live,
    pytest.mark.defense_db,
    allure.epic("ЗАГС"),
    allure.feature("БД: Даниил"),
]


@allure.title("Заявка из API существует в PostgreSQL")
def test_daniil_api_matches_database(defense_api, defense_db):
    response = defense_api.get_applications(limit=1)
    check_status_code(response, expected=200)
    rows = check_applications_body(read_json_object(response))
    if not rows:
        pytest.skip("No existing application; this test does not create records")
    source = rows[0]
    with allure.step("Прочитать заявку из reg_office.applications"):
        row = defense_db.application(source["applicationid"])
    assert row is not None, "API returned an ID absent from the configured DB"
    for key in ["applicationid", "applicantid", "citizenid", "kindofapplication"]:
        assert row[key] == source[key], f"API/DB mismatch: {key}"


@pytest.mark.defense_write
@allure.title("Созданный клиент и его заявка сохранены в БД")
def test_daniil_created_client(defense_api, defense_db, defense_log):
    payload = client_payload("daniil")
    person_id, application_id = create_client(defense_api, payload)
    check_person(defense_db.applicant(person_id), payload)
    application = defense_db.application(application_id)
    assert application is not None, "Created application not found"
    assert application["applicantid"] == person_id
    allure.dynamic.parameter("created_application_id", application_id)
    defense_log.info("client persistence checked; application_id=%s", application_id)


@pytest.mark.defense_write
@allure.title("Созданный администратор сохранен в БД")
def test_daniil_created_admin(defense_api, defense_db, defense_log):
    payload = admin_payload("daniil")
    staff_id = create_admin(defense_api, payload)
    check_person(defense_db.staff(staff_id), payload)
    allure.dynamic.parameter("created_staff_id", staff_id)
    defense_log.info("staff persistence checked; staff_id=%s", staff_id)
