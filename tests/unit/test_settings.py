import pytest

from zags.settings import Settings


@pytest.mark.parametrize(
    "credentials,expected_url",
    [
        pytest.param(
            {"username": "demo", "password": "password"},
            "https://demo:password@example.org/app/",
            id="plain-credentials",
        ),
        pytest.param(
            {"username": "demo@example.org", "password": "p:a/ss?# %"},
            "https://demo%40example.org:p%3Aa%2Fss%3F%23%20%25@example.org/app/",
            id="reserved-characters",
        ),
    ],
)
def test_authenticated_url(make_settings, credentials, expected_url):
    settings = make_settings(**credentials)

    assert settings.authenticated_url() == expected_url


def test_settings_repr_hides_credentials(make_settings):
    settings = make_settings()

    assert settings.username not in repr(settings)
    assert settings.password not in repr(settings)


@pytest.mark.parametrize(
    "overrides,error",
    [
        pytest.param({"base_url": "http://example.org/"}, "absolute HTTPS", id="http-url"),
        pytest.param({"base_url": "example.org"}, "absolute HTTPS", id="relative-url"),
        pytest.param(
            {"base_url": "https://u:p@example.org/"}, "Store credentials", id="credentials-in-url"
        ),
        pytest.param({"base_url": "https://example.org/?x=1"}, "query or fragment", id="url-query"),
        pytest.param(
            {"base_url": "https://example.org/#part"}, "query or fragment", id="url-fragment"
        ),
        pytest.param({"username": ""}, "Set ZAGS_USERNAME", id="empty-username"),
        pytest.param({"password": ""}, "Set ZAGS_USERNAME", id="empty-password"),
        pytest.param({"timeout": 0}, "finite positive", id="zero-timeout"),
        pytest.param({"timeout": -1}, "finite positive", id="negative-timeout"),
        pytest.param({"timeout": float("inf")}, "finite positive", id="infinite-timeout"),
        pytest.param({"timeout": float("nan")}, "finite positive", id="nan-timeout"),
    ],
)
def test_invalid_settings_are_rejected(make_settings, overrides, error):
    with pytest.raises(ValueError, match=error):
        make_settings(**overrides)


@pytest.mark.parametrize("timeout", [15, 8.5], ids=["integer-timeout", "fractional-timeout"])
def test_load_from_environment(monkeypatch, settings_data, timeout):
    expected = settings_data | {"timeout": timeout}
    for key, value in expected.items():
        monkeypatch.setenv(f"ZAGS_{key.upper()}", str(value))

    actual = Settings.from_env()

    assert actual == Settings(**expected)
