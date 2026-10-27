"""Failure diagnostics shared by UI fixtures."""

import warnings
from pathlib import Path
from uuid import uuid4

import allure
from selenium.webdriver.remote.webdriver import WebDriver


def attach_failure_screenshot(driver: WebDriver, directory: Path | None = None) -> None:
    """Attach a PNG and optionally save it locally without masking the test failure."""
    try:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(
            screenshot, name="Скриншот при падении", attachment_type=allure.attachment_type.PNG
        )
        if directory is not None:
            directory.mkdir(parents=True, exist_ok=True)
            (directory / f"failure-{uuid4().hex}.png").write_bytes(screenshot)
    except Exception as error:
        warnings.warn(f"Could not capture screenshot ({type(error).__name__})", stacklevel=2)
