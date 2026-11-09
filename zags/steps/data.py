import allure

from zags.pages.data_page import DataPage
from zags.pages.status_page import StatusPage


@allure.step("Заполнить данные услуги (дата регистрации и данные супруга)")
def fill_service_data(
    page: DataPage,
    reg_date: str,
    spouse_surname: str,
    spouse_name: str,
    spouse_patronymic: str,
    spouse_birth_date: str,
    spouse_passport: str,
    new_surname: str | None = None,
) -> None:
    page.fill_reg_data(reg_date)
    if new_surname is not None:
        page.fill_new_surname(new_surname)
    page.fill_surname_sup(spouse_surname)
    page.fill_name_sup(spouse_name)
    page.fill_lastname_sup(spouse_patronymic)
    page.fill_birth_date(spouse_birth_date)
    page.fill_pasport(spouse_passport)


@allure.step("Нажать кнопку 'Завершить'")
def click_finish(page: DataPage) -> StatusPage:
    return page.click_finish()
