import allure
import pytest
from selenium import webdriver

from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.projects_page import ProjectsPage


@pytest.fixture
def driver():
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    browser.quit()


@allure.title("Отображение кнопки создания проекта после входа")
def test_add_project_button_is_visible(driver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_sign_in()
    login_page.login()

    projects_page = ProjectsPage(driver)

    assert projects_page.is_add_project_button_visible(), (
        "Кнопка создания проекта не отображается"
    )
