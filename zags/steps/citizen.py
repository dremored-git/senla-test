from zags.pages.citizen_page import CitizenPage


def fill_citizen_data(page: CitizenPage, birth_date: str, address: str) -> None:
    page.fill_birth_date(birth_date)
    page.fill_address(address)

def click_next_on_citizen(page: CitizenPage) -> None:
    page.click_next()
