from types import SimpleNamespace

import pytest

from zags.steps.admin import (
    check_admin_form_closed,
    check_admin_surname,
    check_next_button_enabled,
    check_required_fields_empty,
)


@pytest.mark.parametrize(
    "step,method,value,parameters",
    [
        pytest.param(
            check_admin_surname, "surname_value", "Training", {"expected": "Training"}, id="surname"
        ),
        pytest.param(
            check_required_fields_empty,
            "required_values",
            ["", ""],
            {"expected_count": 2},
            id="empty-fields",
        ),
        pytest.param(
            check_next_button_enabled,
            "next_is_enabled",
            False,
            {"expected": False},
            id="disabled-button",
        ),
        pytest.param(check_admin_form_closed, "is_open", False, {}, id="closed-form"),
    ],
)
def test_check_step_accepts_expected_state(step, method, value, parameters):
    page = SimpleNamespace(**{method: lambda: value})

    step(page, **parameters)


@pytest.mark.parametrize(
    "step,method,value,parameters,message",
    [
        pytest.param(
            check_admin_surname,
            "surname_value",
            "wrong",
            {"expected": "Training"},
            "Surname",
            id="wrong-surname",
        ),
        pytest.param(
            check_required_fields_empty,
            "required_values",
            [""],
            {"expected_count": 2},
            "Required fields",
            id="wrong-field-count",
        ),
        pytest.param(
            check_required_fields_empty,
            "required_values",
            ["filled"],
            {"expected_count": 1},
            "not empty",
            id="filled-field",
        ),
        pytest.param(
            check_next_button_enabled,
            "next_is_enabled",
            True,
            {"expected": False},
            "Next button",
            id="enabled-button",
        ),
        pytest.param(check_admin_form_closed, "is_open", True, {}, "still open", id="open-form"),
    ],
)
def test_check_step_rejects_unexpected_state(step, method, value, parameters, message):
    page = SimpleNamespace(**{method: lambda: value})

    with pytest.raises(AssertionError, match=message):
        step(page, **parameters)
