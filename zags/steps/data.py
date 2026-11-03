import allure

from zags.pages.data_page import DataPage


@allure.step("Заполнить данные услуги (дата регистрации и данные супруга)")
def fill_service_data(
    page: DataPage,
    reg_date: str,
    spouse_surname: str,
    spouse_name: str,
    spouse_patronymic: str,
    spouse_birth_date: str,
    spouse_passport: str,
) -> None:
    page.fill_reg_data(reg_date)
    page.fill_spouse_data(
        surname=spouse_surname,
        name=spouse_name,
        patronymic=spouse_patronymic,
        birth_date=spouse_birth_date,
        passport=spouse_passport
    )

@allure.step("Нажать кнопку 'Завершить'")
def click_finish(page: DataPage) -> None:
    page.click_finish()
