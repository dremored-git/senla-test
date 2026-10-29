from pathlib import Path

import pytest
from selenium import webdriver

from zags.reporting import attach_failure_screenshot

REPORTS = pytest.StashKey[dict]()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    report = (yield).get_result()
    item.stash.setdefault(REPORTS, {})[report.when] = report


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
        save_locally = request.config.getoption("--screenshot-on-failure")
        allure_enabled = request.config.getoption("allure_report_dir", default=None)
        if failed and (allure_enabled or save_locally):
            directory = Path(request.config.rootpath) / "artifacts" if save_locally else None
            attach_failure_screenshot(browser_driver, directory)
        browser_driver.quit()
