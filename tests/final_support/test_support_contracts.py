import pytest
from sqlalchemy import create_engine, text

from zags.defense.api_steps import check_person, client_payload, created_id
from zags.defense.db import Database


def test_payloads_are_unique():
    first, second = client_payload("Roman"), client_payload("Roman")
    assert first["personalNumberOfPassport"] != second["personalNumberOfPassport"]
    assert first["mode"] == "birth"


@pytest.mark.parametrize("value", [None, "null", "", True, 0, -1])
def test_missing_or_invalid_id_fails(value):
    with pytest.raises(AssertionError, match="positive"):
        created_id({"data": {"applicationid": value}}, "applicationid")


def test_id_from_real_response_envelope():
    assert created_id({"data": {"staffid": 42}}, "staffid") == 42


def test_check_person_detects_wrong_persistence():
    payload = client_payload("Roman")
    with pytest.raises(AssertionError, match="surname"):
        check_person({"surname": "Wrong"}, payload)


def test_parameterized_query_does_not_interpolate_input():
    engine = create_engine("sqlite://")
    database = Database(engine)
    try:
        with engine.begin() as c:
            c.execute(text("CREATE TABLE people (id TEXT, name TEXT)"))
            c.execute(
                text("INSERT INTO people VALUES (:id, :name)"), {"id": "safe", "name": "Expected"}
            )
        assert (
            database._one("SELECT name FROM people WHERE id=:identifier", identifier="' OR 1=1 --")
            is None
        )
        assert database._one("SELECT name FROM people WHERE id=:identifier", identifier="safe") == {
            "name": "Expected"
        }
    finally:
        database.close()
