import base64
import json
from urllib.parse import parse_qs, urlsplit

import pytest
from requests import Response, Session, Timeout

from zags.api.client import NoAuth, ZagsApi
from zags.steps.api import get_applications


@pytest.fixture
def sent_requests(monkeypatch):
    calls = []

    def send(session, request, **kwargs):
        calls.append((request, kwargs))
        response = Response()
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response._content = b'{"data": []}'
        response.request = request
        return response

    monkeypatch.setattr(Session, "send", send)
    return calls


def test_get_prepares_basic_auth_query_and_timeout(make_settings, sent_requests):
    client = ZagsApi(make_settings(timeout=7))
    try:
        response = client.get_applications(limit=3, offset=2)
    finally:
        client.close()

    assert response.status_code == 200
    assert len(sent_requests) == 1
    request, options = sent_requests[0]
    url = urlsplit(request.url)
    assert request.method == "GET"
    assert url.path == "/app/getApplications"
    assert parse_qs(url.query) == {"limit": ["3"], "offset": ["2"]}
    expected = base64.b64encode(b"test-user:test-password").decode()
    assert request.headers["Authorization"] == "Basic " + expected
    assert options["timeout"] == 7
    assert options["verify"] is True


def test_explicit_no_auth_sends_no_authorization(make_settings, sent_requests):
    client = ZagsApi(make_settings(), auth=NoAuth())
    try:
        client.get_applications()
    finally:
        client.close()

    request, _ = sent_requests[0]
    assert "Authorization" not in request.headers


def test_post_serializes_json_body(make_settings, sent_requests):
    payload = {"personalFirstName": "Учебный", "dateofbirth": "1990-01-01"}
    client = ZagsApi(make_settings())
    try:
        client.create_admin(payload)
    finally:
        client.close()

    request, options = sent_requests[0]
    assert request.method == "POST"
    assert urlsplit(request.url).path == "/app/sendAdminRequest"
    assert request.headers["Content-Type"] == "application/json"
    assert json.loads(request.body) == payload
    assert options["timeout"] == 15


@pytest.mark.parametrize("identifier", [0, -1, True, "12"])
def test_invalid_application_id_is_rejected_before_http(make_settings, sent_requests, identifier):
    client = ZagsApi(make_settings())
    try:
        with pytest.raises(ValueError, match="positive integer"):
            client.get_application_status(identifier)
    finally:
        client.close()
    assert sent_requests == []


def test_transport_timeout_propagates(monkeypatch, make_settings):
    def fail(*args, **kwargs):
        raise Timeout("Deliberate transport timeout")

    monkeypatch.setattr(Session, "send", fail)
    client = ZagsApi(make_settings())
    try:
        with pytest.raises(Timeout, match="Deliberate transport timeout"):
            client.get_applications()
    finally:
        client.close()


def test_allure_step_supports_default_query_parameters(make_settings, sent_requests):
    client = ZagsApi(make_settings())
    try:
        response = get_applications(client)
    finally:
        client.close()
    assert response.status_code == 200
    request, _ = sent_requests[0]
    assert parse_qs(urlsplit(request.url).query) == {"limit": ["2"], "offset": ["0"]}
