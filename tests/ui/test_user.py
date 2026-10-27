import allure
import pytest

from zags.pages.citizen_page import CitizenPage
from zags.pages.data_page import DataPage
from zags.pages.status_page import StatusPage
from zags.steps.navigation import open_zags
from zags.steps.status import check_application_number_not_empty, check_application_status
from zags.steps.user import open_user_form

pytestmark = [pytest.mark.ui]
@allure.epic("ЗАГС")
@allure.feature("Пользователь")
@allure.story("Ввод и очистка фамилии")
@allure.title("Ввод и очистка фамилии: {param_id}")

def test_open_user_form_and_fill_surname(driver, settings):
    
    home = open_zags(driver, settings)
    user_page = open_user_form(home)   
    user_page.fill_surname("Иванов")
    user_page.fill_name("Иван")
    user_page.fill_lastname("Ivanovich")
    user_page.fill_telephon("37512312312")
    user_page.fill_pasport("КВ123123")
    user_page.fill_address("г. Москва, ул. Ленина, д. 1")

    user_page.click_next()
    user_page.click_brak() 

    citizen = CitizenPage(driver, settings.timeout)
    citizen.wait_until_open()
    citizen.fill_surname("Иванов")
    citizen.fill_name("Иван")
    citizen.fill_lastname("Ivanovich")
    citizen.fill_data("01-01-1990")
    citizen.fill_pasport("КВ123123")
    citizen.fill_gender("Муж")
    citizen.fill_address("г. Москва, ул. Ленина, д. 1")
    citizen.click_next()

    data = DataPage(driver, settings.timeout)
    data.wait_until_open()
    data.fill_reg_data("10-10-2010")
    data.fill_new_surname("Акимов")
    data.fill_surname_sup("Пыткова")
    data.fill_name_sup("Анастасия")
    data.fill_lastname_sup("Сергеевна")
    data.fill_birth_date("01-12-2011")
    data.fill_pasport("ВУ123123")

    data.click_finish()

    status_page = StatusPage(driver, settings.timeout)
    status_page.wait_until_open()
    check_application_number_not_empty(status_page)
    check_application_status(status_page, expected_status="На рассмотрении.")