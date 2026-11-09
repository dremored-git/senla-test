import json

import pytest
from requests import Response

from zags.steps.api import (
    check_application_status_body,
    check_applications_body,
    check_created_admin,
    check_status_code,
    read_json_object,
)


@pytest.mark.parametrize(
    "check,body",
    [
        pytest.param(check_applications_body, {"data": {}}, id="list-is-object"),
        pytest.param(check_applications_body, {"data": [{"applicationid": None}]}, id="null-id"),
        pytest.param(check_applications_body, {"data": [{"applicationid": True}]}, id="boolean-id"),
        pytest.param(check_application_status_body, {"data": []}, id="status-is-list"),
        pytest.param(check_application_status_body, {"data": {}}, id="status-fields-missing"),
        pytest.param(check_created_admin, {"data": {"staffid": None}}, id="null-staff-id"),
    ],
)
def test_api_check_rejects_invalid_body(check, body):
    with pytest.raises(AssertionError):
        check(body)


@pytest.mark.parametrize(
    "status,content_type,body",
    [
        pytest.param(200, "text/html", "<p>VPN required</p>", id="html-instead-of-json"),
        pytest.param(200, "application/json", "not JSON", id="invalid-json"),
        pytest.param(200, "application/json", "[]", id="wrong-root-type"),
    ],
)
def test_read_json_rejects_invalid_response(status, content_type, body):
    response = Response()
    response.status_code = status
    response.headers["Content-Type"] = content_type
    response._content = body.encode()
    with pytest.raises(AssertionError):
        read_json_object(response)


def test_status_check_does_not_accept_wrong_http_code():
    response = Response()
    response.status_code = 401
    with pytest.raises(AssertionError, match="expected 200, got 401"):
        check_status_code(response, expected=200)


def test_json_reader_accepts_charset_header():
    response = Response()
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response._content = json.dumps({"data": []}).encode()
    assert read_json_object(response) == {"data": []}
