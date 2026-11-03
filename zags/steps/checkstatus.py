from zags.pages.statusapp import AppStatuspage


def check_application_number_not_empty(page: AppStatuspage) -> None:
    actual_number = page.get_application_number()
    assert actual_number != "", "Номер заявки пустой!"
    assert actual_number.isdigit(), f"Номер заявки содержит не только цифры: {actual_number}"


def check_application_status(page: AppStatuspage, expected_status: str) -> None:
    actual_status = page.get_status()
    assert actual_status == expected_status, (
        f"Статус: ожидался {expected_status!r}, получен {actual_status!r}"
    )
