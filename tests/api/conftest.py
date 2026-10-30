import pytest
from requests.auth import HTTPBasicAuth

from zags.api.client import NoAuth, ZagsApi
from zags.steps.api import (
    check_applications_body,
    check_status_code,
    get_applications,
    read_json_object,
    check_app_id_is_correct
)


@pytest.fixture
def api_client(settings):
    client = ZagsApi(settings)
    yield client
    client.close()


@pytest.fixture(
    params=[NoAuth(), HTTPBasicAuth("invalid-training-user", "invalid-training-password")],
    ids=["missing-auth", "invalid-auth"],
)
def unauthorized_api_client(request, settings):
    client = ZagsApi(settings, auth=request.param)
    yield client
    client.close()


@pytest.fixture
def existing_application_id(api_client):
    response = get_applications(api_client, limit=1)
    check_status_code(response, expected=200)
    rows = check_applications_body(read_json_object(response))
    if not rows:
        pytest.skip("No application exists on the stand; this read-only fixture creates none")
    return rows[0]["applicationid"]


@pytest.fixture
def existing_applications_id_test_roman(api_client):
    response = get_applications(api_client, limit=10)
    check_status_code(response, expected=200)
    rows = check_app_id_is_correct(read_json_object(response))
    if not rows:
        pytest.skip("No application exists on the stand; this read-only fixture creates none")
    return rows["applicationid"]
