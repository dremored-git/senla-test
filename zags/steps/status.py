from zags.pages.status_page import StatusPage

def check_application_number_not_empty(page: StatusPage) -> None:
    actual_number = page.get_application_number()
    assert actual_number != "", "Номер заявки пустой!"
    assert actual_number.isdigit(), f"Номер заявки содержит не только цифры: {actual_number}"

def check_application_status(page: StatusPage, expected_status: str) -> None:
    actual_status = page.get_status()
    assert actual_status == expected_status, f"Статус: ожидался {expected_status!r}, получен {actual_status!r}"