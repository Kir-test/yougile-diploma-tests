import uuid

import allure
import pytest

from ui_tests.pages.company_page import CompanyPage


@pytest.fixture
def invited_email(logged_in_driver, screenshot):
    """Уникальный адрес на каждый запуск; после теста сотрудник удаляется, даже если тест упал."""
    email = f"kirskytest+{uuid.uuid4().hex[:8]}@gmail.com"
    yield email

    with allure.step(f"Очистка: удалить сотрудника {email}, если он остался"):
        logged_in_driver.refresh()  # закрыть возможные окна после падения теста
        company = CompanyPage(logged_in_driver)
        company.open()
        screenshot("Очистка — открыта страница компании")
        if company.has_employee(email):
            company.delete_employee(email)
            screenshot("Очистка — сотрудник удалён")


@allure.epic("Yougile")
@allure.feature("Сотрудники")
@allure.title("Приглашение сотрудника в компанию по почте")
@allure.severity(allure.severity_level.CRITICAL)
def test_invite_employee_by_email(logged_in_driver, invited_email, screenshot) -> None:
    company = CompanyPage(logged_in_driver)

    with allure.step("Открыть раздел 'Компания'"):
        company.open()
        screenshot("01 — Раздел 'Компания' открыт")

    with allure.step(f"Пригласить сотрудника {invited_email}"):
        company.invite_employee(invited_email)
        screenshot("02 — Форма приглашения заполнена и отправлена")

    with allure.step("Проверить, что показано уведомление об успехе"):
        assert company.is_invite_success_shown(), "Нет уведомления об успешном приглашении"
        screenshot("03 — Уведомление об успехе")

    with allure.step("Проверить, что сотрудник появился в списке"):
        assert company.is_employee_in_list(invited_email), (
            f"Сотрудник {invited_email} не появился в списке компании"
        )
        screenshot("04 — Сотрудник в списке компании")
