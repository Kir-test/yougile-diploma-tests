from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import UI_EMAIL, UI_PASSWORD, UI_BASE_URL


class LoginPage:
    SIGN_IN_LINK = (By.CSS_SELECTOR, "a.sign-in-button")
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    LOGIN_BUTTON = (
        By.XPATH,
        '//div[@role="button" and .//div[normalize-space()="Войти"]]',
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def open(self) -> None:
        self.driver.get(UI_BASE_URL)

    def click_sign_in(self) -> None:
        sign_in_link = self.wait.until(
            EC.element_to_be_clickable(self.SIGN_IN_LINK)
        )
        sign_in_link.click()

    def login(self) -> None:
        if not UI_EMAIL or not UI_PASSWORD:
            raise ValueError(
                "Укажи UI_EMAIL и UI_PASSWORD в config/.env"
            )

        email_input = self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_input.send_keys(UI_EMAIL)

        password_input = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        password_input.send_keys(UI_PASSWORD)

        login_button = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
