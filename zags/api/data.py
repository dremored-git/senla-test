"""Only synthetic data for the optional write example."""

from uuid import uuid4


def make_admin_payload(**overrides) -> dict:
    payload = {
        "dateofbirth": "1990-01-01",
        "personalFirstName": "Учебный",
        "personalLastName": "API" + uuid4().hex[:8],
        "personalMiddleName": "Тестович",
        "personalNumberOfPassport": "TEST" + uuid4().hex[:8],
        "personalPhoneNumber": "00000000000",
    }
    return payload | overrides
