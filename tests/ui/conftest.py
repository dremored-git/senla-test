import warnings
from pathlib import Path
from uuid import uuid4

import pytest
from dotenv import load_dotenv
from selenium import webdriver

from zags.settings import Settings

REPORTS = pytest.StashKey[dict]()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    item.stash.setdefault(REPORTS, {})[report.when] = report


@pytest.fixture
def settings():
    load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)
    return Settings.from_env()


@pytest.fixture
def driver(request, settings):
    browser = request.config.getoption("--browser")
    options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.EdgeOptions()
    options.add_argument("--lang=ru-RU")
    options.add_argument("--window-size=1440,1000")
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    factory = webdriver.Chrome if browser == "chrome" else webdriver.Edge
    browser_driver = factory(options=options)
    try:
        browser_driver.set_page_load_timeout(45)
        yield browser_driver
    finally:
        reports = request.node.stash.get(REPORTS, {})
        failed = any(report.failed for report in reports.values())
        if failed and request.config.getoption("--screenshot-on-failure"):
            try:
                directory = Path(request.config.rootpath) / "artifacts"
                directory.mkdir(exist_ok=True)
                browser_driver.save_screenshot(str(directory / f"failure-{uuid4().hex}.png"))
            except Exception as error:
                warnings.warn(f"Could not save screenshot ({type(error).__name__})", stacklevel=2)
        browser_driver.quit()
