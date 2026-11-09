import logging
import os
from pathlib import Path

import allure
import pytest

REPORTS = pytest.StashKey[dict]()


def pytest_addoption(parser):
    parser.addoption(
        "--allow-defense-writes",
        action="store_true",
        help="Allow final training examples to create stand records",
    )


def pytest_configure(config):
    for marker in [
        "defense_live: live stand/VPN required",
        "defense_write: creates records; requires --allow-defense-writes",
        "defense_db: API and PostgreSQL integration",
        "defense_pw: Playwright examples",
        "defense_remote: remote Selenium examples",
    ]:
        config.addinivalue_line("markers", marker)


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--allow-defense-writes"):
        for item in items:
            if "defense_write" in item.keywords:
                item.add_marker(
                    pytest.mark.skip(
                        reason="Explicitly enable creation with --allow-defense-writes"
                    )
                )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    item.stash.setdefault(REPORTS, {})[report.when] = report


@pytest.fixture
def defense_api(settings):
    from zags.defense.api_steps import RegistrationApi

    client = RegistrationApi(settings)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def defense_db(settings):
    from zags.defense.db import Database

    database = Database.from_env()
    try:
        database.application(-1)  # SELECT preflight before any HTTP write
        yield database
    finally:
        database.close()


@pytest.fixture
def defense_page(settings, request):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            http_credentials={"username": settings.username, "password": settings.password},
            locale="ru-RU",
            viewport={"width": 1440, "height": 1000},
        )
        page = context.new_page()
        page.set_default_timeout(settings.timeout * 1000)
        try:
            yield page
        finally:
            reports = request.node.stash.get(REPORTS, {})
            if any(r.failed for r in reports.values()):
                try:
                    allure.attach(
                        page.screenshot(),
                        name="Playwright failure",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception as error:
                    logging.getLogger(__name__).warning(
                        "Screenshot unavailable: %s", type(error).__name__
                    )
            context.close()
            browser.close()


@pytest.fixture
def defense_remote_driver(settings):
    from selenium import webdriver

    endpoint = os.environ.get("ZAGS_REMOTE_URL")
    if not endpoint:
        raise ValueError("Set ZAGS_REMOTE_URL, for example http://localhost:4444/wd/hub")
    options = webdriver.ChromeOptions()
    options.browser_version = os.getenv("ZAGS_REMOTE_VERSION", "128.0")
    options.set_capability("selenoid:options", {"enableVNC": True})
    driver = webdriver.Remote(command_executor=endpoint, options=options)
    driver.set_page_load_timeout(45)
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
def defense_log(tmp_path):
    path = Path(tmp_path) / "training.log"
    logger = logging.getLogger("zags.defense")
    old_level = logger.level
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    try:
        yield logger
    finally:
        handler.close()
        logger.removeHandler(handler)
        logger.setLevel(old_level)
        allure.attach(
            path.read_text(encoding="utf-8"),
            name="Training log",
            attachment_type=allure.attachment_type.TEXT,
        )
