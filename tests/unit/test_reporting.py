from types import SimpleNamespace
from unittest.mock import Mock

import allure
import pytest

from zags.reporting import attach_failure_screenshot


@pytest.mark.parametrize("save_locally", [False, True], ids=["report-only", "with-local-copy"])
def test_failure_screenshot_attached_as_png(monkeypatch, tmp_path, save_locally):
    screenshot = b"test-screenshot-bytes"
    driver = SimpleNamespace(get_screenshot_as_png=lambda: screenshot)
    attach = Mock()
    monkeypatch.setattr(allure, "attach", attach)
    directory = tmp_path / "artifacts" if save_locally else None

    attach_failure_screenshot(driver, directory)

    attach.assert_called_once_with(
        screenshot, name="Скриншот при падении", attachment_type=allure.attachment_type.PNG
    )
    files = list(tmp_path.rglob("*.png"))
    assert len(files) == int(save_locally)
    if save_locally:
        assert files[0].read_bytes() == screenshot


def test_screenshot_failure_does_not_replace_original_error(monkeypatch):
    driver = SimpleNamespace(get_screenshot_as_png=Mock(side_effect=RuntimeError("closed browser")))
    attach = Mock()
    monkeypatch.setattr(allure, "attach", attach)

    with pytest.warns(UserWarning, match=r"Could not capture screenshot \(RuntimeError\)"):
        attach_failure_screenshot(driver)

    attach.assert_not_called()
