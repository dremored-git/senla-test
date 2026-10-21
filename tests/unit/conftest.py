import pytest

from zags.settings import Settings


@pytest.fixture
def settings_data():
    return {
        "base_url": "https://example.org/app/",
        "username": "test-user",
        "password": "test-password",
        "timeout": 15,
    }


@pytest.fixture
def make_settings(settings_data):
    def create(**overrides):
        return Settings(**(settings_data | overrides))

    return create
