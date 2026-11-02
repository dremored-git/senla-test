import logging
import re

import allure
from playwright.sync_api import expect

LOG = logging.getLogger(__name__)


class RegistrationPage:
    def __init__(self, page):
        self.page = page
        self.dialog = page.get_by_role("dialog")

    def field(self, caption):
        # React form: label sits in a caption div directly before its input.
        label = self.dialog.locator("label").filter(
            has_text=re.compile(r"^" + re.escape(caption) + r"\s*\*?$")
        )
        field = label.locator("xpath=../following-sibling::input")
        expect(field).to_have_count(1)
        return field

    def fill_fields(self, values):
        for caption, value in values.items():
            self.field(caption).fill(value)

    def button(self, caption):
        return self.dialog.get_by_role("button", name=caption, exact=True)


@allure.step("Открыть форму регистрации пользователя")
def open_registration(page, settings):
    page.goto(settings.base_url, wait_until="domcontentloaded")
    page.get_by_role("button", name="Войти как пользователь", exact=True).click()
    form = RegistrationPage(page)
    expect(form.dialog).to_be_visible()
    return form


@allure.step("Заполнить данные заявителя")
def fill_applicant(form, passport):
    form.fill_fields(
        {
            "Фамилия": "Учебный",
            "Имя": "Тест",
            "Отчество": "Тестович",
            "Телефон": "00000000000",
            "Номер паспорта": passport,
            "Адрес прописки": "Учебный адрес 1",
        }
    )
    form.button("Далее").click()


@allure.step("Выбрать услугу")
def choose_service(form, service):
    form.button(service).click()


@allure.step("Заполнить данные гражданина")
def fill_citizen(form):
    form.fill_fields(
        {
            "Фамилия": "Учебный",
            "Имя": "Тест",
            "Отчество": "Тестович",
            "Дата рождения": "1990-01-01",
            "Номер паспорта": "TS900001",
            "Пол": "муж",
            "Адрес прописки": "Учебный адрес 1",
        }
    )
    form.button("Далее").click()


@allure.step("Заполнить данные услуги")
def fill_service(form, service):
    if service == "birth":
        form.fill_fields(
            {
                "Место рождения": "Учебный город",
                "Мать": "Тестовая мать",
                "Отец": "Тестовый отец",
                "Бабушка": "Тестовая бабушка",
                "Дедушка": "Тестовый дедушка",
            }
        )
    elif service == "wedding":
        form.fill_fields(
            {
                "Дата регистрации": "2026-01-01",
                "Новая фамилия": "Учебная",
                "Фамилия супруга/и": "Учебная",
                "Имя супруга/и": "Тест",
                "Отчество супруга/и": "Тестовна",
                "Дата рождения супруга/и": "1991-01-01",
                "Номер паспорта супруга/и": "TS910001",
            }
        )
    else:
        raise ValueError("Unsupported training service")


@allure.step("Отправить заявку и проверить реальный номер")
def submit_registration(form):
    with form.page.expect_response(
        lambda r: r.request.method == "POST" and r.url.endswith("/sendUserRequest")
    ) as captured:
        form.button("Завершить").click()
    response = captured.value
    LOG.info("registration completed: HTTP %s", response.status)
    assert response.status == 200, f"Registration HTTP {response.status}"
    from zags.defense.api_steps import created_id

    identifier = created_id(response.json(), "applicationid")
    expect(form.dialog).to_contain_text(f"Ваша заявка № {identifier} ")
    expect(form.dialog).to_contain_text("На рассмотрении")
    return identifier
