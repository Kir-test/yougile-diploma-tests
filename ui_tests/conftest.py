import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui_tests.pages.login_page import LoginPage

LEFT_SIDEBAR = (By.CSS_SELECTOR, '[data-testid="left-sidebar"]')

# Папка для сохранения скриншотов (прикладывается к диплому)
SCREENSHOTS_DIR = "screenshots"


def make_step_screenshot(driver, name: str) -> None:
    """Сохраняет скриншот в папку screenshots/ и прикрепляет его к Allure-отчёту.

    :param driver: Selenium WebDriver
    :param name: человекочитаемое имя шага (будет и именем файла, и подписью в Allure)
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    safe_name = (
        name.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )[:80]
    filepath = os.path.join(SCREENSHOTS_DIR, f"{safe_name}.png")
    driver.save_screenshot(filepath)
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )

@pytest.fixture
def screenshot(driver):
    """Фикстура-обёртка: делает скриншот + сохраняет в screenshots/ + цепляет в Allure.

    Использование в тесте:
        with allure.step("..."):
            ...
            screenshot("имя_шага")
    """
    def _make(name: str) -> None:
        make_step_screenshot(driver, name)
    return _make

@pytest.fixture
def driver(request):
    browser = webdriver.Chrome()
    browser.maximize_window()
    request.node._driver = browser
    yield browser
    browser.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Браузер, в котором уже выполнен вход через форму."""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.click_sign_in()
    login_page.login()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located(LEFT_SIDEBAR))
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Прикладывает скриншот к Allure-отчёту и сохраняет в screenshots/, если тест упал."""
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        browser = getattr(item, "_driver", None) or item.funcargs.get("driver")
        if browser:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            filepath = os.path.join(SCREENSHOTS_DIR, f"FAIL_{item.name}.png")
            try:
                browser.save_screenshot(filepath)
            except Exception:
                pass  # браузер мог уже закрыться
            allure.attach(
                browser.get_screenshot_as_png(),
                name=f"Скриншот при падении: {item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
