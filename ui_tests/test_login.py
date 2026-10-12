
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.projects_page import ProjectsPage


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@allure.title("Отображение формы авторизации")
def test_login_form_is_displayed(driver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_sign_in()

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(
        EC.visibility_of_element_located(LoginPage.EMAIL_INPUT)
    )
    password_input = wait.until(
        EC.visibility_of_element_located(LoginPage.PASSWORD_INPUT)
    )

    assert email_input.is_displayed()
    assert password_input.is_displayed()


@allure.title("Успешный вход в YouGile")
def test_login_is_successful(driver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_sign_in()
    login_page.login()

    projects_page = ProjectsPage(driver)

    assert projects_page.is_add_project_button_visible(), (
        "После авторизации не появилась кнопка создания проекта"
    )
