"""Small HTTP client: endpoints and transport, without test assertions."""

import json

import allure
from requests import Response, Session
from requests.auth import AuthBase, HTTPBasicAuth

from zags.settings import Settings


class NoAuth(AuthBase):
    """Explicitly send no credentials, including credentials from a local netrc."""

    def __call__(self, request):
        return request


class ZagsApi:
    def __init__(self, settings: Settings, *, auth: AuthBase | None = None):
        self._base_url = settings.base_url.rstrip("/")
        self._timeout = settings.timeout
        self._session = Session()
        self._session.auth = (
            HTTPBasicAuth(settings.username, settings.password) if auth is None else auth
        )
        self._session.headers.update({"Accept": "application/json"})

    def get_applications(self, *, limit: int = 2, offset: int = 0) -> Response:
        return self._request("GET", "/getApplications", params={"limit": limit, "offset": offset})

    def get_application_status(self, application_id: int) -> Response:
        if type(application_id) is not int or application_id <= 0:
            raise ValueError("application_id must be a positive integer")
        return self._request("GET", f"/getApplStatus/{application_id}")

    def create_admin(self, payload: dict) -> Response:
        return self._request("POST", "/sendAdminRequest", json=payload)

    def close(self) -> None:
        self._session.close()

    def _request(self, method: str, path: str, **kwargs) -> Response:
        response = self._session.request(
            method, self._base_url + path, timeout=self._timeout, **kwargs
        )
        # Keep Basic Auth, personal data and full response bodies out of the report.
        allure.attach(
            json.dumps(
                {
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "content_type": response.headers.get("Content-Type", ""),
                },
                ensure_ascii=False,
                indent=2,
            ),
            name="HTTP response metadata",
            attachment_type=allure.attachment_type.JSON,
        )
        return response
