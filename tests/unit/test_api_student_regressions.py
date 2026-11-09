from unittest.mock import create_autospec

import pytest

from zags.api.client import ZagsApi
from zags.steps.api import (
    check_app_id_is_correct,
    check_application_kindofstatus,
    check_applications_body,
    check_created_admin,
    get_applications_length_limit,
)


@pytest.mark.parametrize("data", [None, {}, [{"applicationid": True}], [{"applicationid": 0}]])
def test_malformed_list_is_failure_instead_of_skip(data):
    with pytest.raises(AssertionError):
        check_applications_body({"data": data})


def test_empty_list_is_a_valid_response():
    assert check_applications_body({"data": []}) == []


def test_list_ids_are_integers_not_objects():
    rows = [{"applicationid": 42}]
    assert check_app_id_is_correct({"data": rows}) == rows


def test_limit_check_uses_existing_response_without_another_request():
    api = create_autospec(ZagsApi, instance=True, spec_set=True)
    rows = [{"applicationid": 42}]
    assert get_applications_length_limit(api, {"data": rows}, limit=1) == rows
    api.get_applications.assert_not_called()
    with pytest.raises(AssertionError, match="at most 0"):
        get_applications_length_limit(api, {"data": rows}, limit=0)


def test_kind_check_compares_with_independent_list_value():
    body = {"data": {
        "dateofapplication": "2026-11-09",
        "kindofapplication": "Регистрация рождения",
        "statusofapplication": "На рассмотрении",
    }}
    check_application_kindofstatus(body, expected="Регистрация рождения")
    with pytest.raises(AssertionError, match="Expected application kind"):
        check_application_kindofstatus(body, expected="Регистрация брака")


def test_created_admin_uses_actual_response_envelope():
    assert check_created_admin({"data": {"staffid": 42}}) == 42
    with pytest.raises(AssertionError, match="response.data"):
        check_created_admin({"staffid": 42})
