from pathlib import Path

import pytest
from dotenv import load_dotenv

from zags.settings import Settings

pytest_plugins = ["zags.fixtures.api", "zags.fixtures.browser"]


def pytest_addoption(parser):
    parser.addoption(
        "--allow-api-writes", action="store_true", help="Allow API tests that create records"
    )
    parser.addoption(
        "--headless", action="store_true", help="Run UI tests without a browser window"
    )
    parser.addoption("--browser", choices=["chrome", "edge"], default="chrome")
    parser.addoption(
        "--screenshot-on-failure", action="store_true", help="Save failed UI screenshots locally"
    )


@pytest.fixture
def settings():
    load_dotenv(Path(__file__).resolve().parents[1] / ".env", override=False)
    return Settings.from_env()


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--allow-api-writes"):
        skip = pytest.mark.skip(reason="Creates records: enable explicitly with --allow-api-writes")
        for item in items:
            if "api_write" in item.keywords:
                item.add_marker(skip)
