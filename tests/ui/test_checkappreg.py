import pytest

from zags.pages.appdata import AppData
from zags.pages.application_choice import Application_choice
from zags.pages.Citizen_data import CitizenData
from zags.pages.statusapp import AppStatuspage
from zags.steps.checkstatus import check_application_number_not_empty, check_application_status
from zags.steps.navigation import open_zags
from zags.steps.user import open_user_form

pytestmark = [pytest.mark.ui]


def test_open_user_form_and_fill_surname(driver, settings):

    home = open_zags(driver, settings)
    user_page = open_user_form(home)
    user_page.set_surname("Иванов")
    user_page.set_firstname("Иван")
    user_page.set_thirdname("Ivanovich")
    user_page.set_phone("37512312312")
    user_page.set_passport("КВ123123")
    user_page.set_adress("г. Москва, ул. Ленина, д. 1")

    user_page.next()
    app_choice = Application_choice(driver)  # или Application_choice(driver, settings.timeout)
    app_choice.birthapp_choice()

    citizen = CitizenData(driver, settings.timeout)
    citizen.wait_until_open()
    citizen.set_lastname("Иванов")
    citizen.set_firstname("Иван")
    citizen.set_surname("Ivanovich")
    citizen.set_birthdate("01.01.1990")
    citizen.set_passport("КВ123123")
    citizen.set_gender("Муж")
    citizen.set_adress("г. Москва, ул. Ленина, д. 1")
    citizen.next()

    data = AppData(driver, settings.timeout)
    data.wait_until_open()
    data.set_birthplace("Grodno")
    data.set_mother("Иванова")
    data.set_father("Иванов")
    data.set_grandmother("Бабуля")
    data.set_grandfather("Дедуля")

    data.finish()

    status_page = AppStatuspage(driver, settings.timeout)
    status_page.wait_until_open()
    check_application_number_not_empty(status_page)
    check_application_status(status_page, expected_status="На рассмотрении.")
