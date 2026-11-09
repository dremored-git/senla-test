from pathlib import Path

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from zags.steps.navigation import open_zags

pytestmark = [pytest.mark.defense_live, pytest.mark.defense_remote]


@allure.title("Удаленный браузер Selenoid: {param_id}")
@pytest.mark.parametrize("slot", ["one", "two", "three"])
def test_roman_three_sessions(defense_remote_driver, settings, slot, tmp_path_factory, testrun_uid):
    # With -n 3 all gw*/ bases have the same parent on this local machine.
    shared = Path(tmp_path_factory.getbasetemp()).parent / ("barrier-" + testrun_uid)
    shared.mkdir(exist_ok=True)
    open_zags(defense_remote_driver, settings)
    (shared / slot).touch()
    with allure.step("Дождаться трех одновременно открытых браузеров"):
        WebDriverWait(defense_remote_driver, 30).until(
            lambda _: len(list(shared.iterdir())) == 3,
            message="Expected 3 ready sessions: run this file alone with -n 3",
        )
    assert defense_remote_driver.session_id, "Remote session was not created"
