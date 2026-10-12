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


@allure.title("Открытие формы создания проекта")
def test_project_creation_modal_is_opened(driver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_sign_in()
    login_page.login()

    projects_page = ProjectsPage(driver)
    projects_page.open_project_creation_modal()

    assert projects_page.is_project_creation_modal_visible(), (
        "Форма создания проекта не отображается"
    )
