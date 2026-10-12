import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CompanyPage:
    # --- раздел «Моя компания» ---
    MY_COMPANY_ITEM = (By.CSS_SELECTOR, '[data-testid="my-company-item"]')
    INVITE_BTN = (By.CSS_SELECTOR, '[data-testid="invite-by-email-button"]')

    # --- окно приглашения ---
    EMAILS_INPUT = (
        By.CSS_SELECTOR,
        '[data-testid="company-invite-popup-emails-input"] textarea',
    )
    # пока кнопка неактивна, у неё класс pointer-events-none (атрибута disabled нет)
    SUBMIT_BTN_ENABLED = (
        By.XPATH,
        '//*[@data-testid="company-invite-popup-submit-button"]'
        '[not(contains(@class, "pointer-events-none"))]',
    )

    # --- уведомление об успехе ---
    # TODO: заменить на data-testid уведомления, когда пришлёшь его HTML
    INVITE_TOAST = (By.XPATH, '//*[contains(normalize-space(.), "успешно пригла")]')

    # --- окно сотрудника и удаление ---
    REMOVE_LINK = (By.CSS_SELECTOR, ".prj-invite__card-remove-btn")
    CONFIRM_DELETE_BTN = (
        By.XPATH,
        '//div[@role="button"][.//div[normalize-space()="Удалить сотрудника"]]',
    )
    BACK_TO_COMPANY_BTN = (
        By.XPATH,
        '//div[@role="button"][.//div[normalize-space()="Назад в Мою компанию"]]',
    )

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, timeout, ignored_exceptions=(StaleElementReferenceException,)
        )

    @staticmethod
    def _employee_row(email):
        # TODO: заменить на data-testid строки таблицы сотрудников
        # Адрес может встречаться в нескольких местах страницы (колонки «Имя» и «E-mail»,
        # скрытые элементы), поэтому берём все совпадения, а видимое выбираем в коде.
        return (By.XPATH, f'//*[normalize-space(text())="{email}"]')

    @staticmethod
    def _deleted_message(email):
        return (
            By.XPATH,
            f'//span[contains(normalize-space(.), "{email}") '
            f'and contains(normalize-space(.), "удален из компании")]',
        )

    def _visible_employee_element(self, email):
        """Первый видимый элемент с адресом сотрудника (прокручивает страницу к нему)."""

        def find(driver):
            for element in driver.find_elements(*self._employee_row(email)):
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )
                if element.is_displayed():
                    return element
            return False

        return self.wait.until(find)

    @allure.step("Открыть раздел «Моя компания»")
    def open(self):
        self.wait.until(EC.element_to_be_clickable(self.MY_COMPANY_ITEM)).click()
        self.wait.until(EC.visibility_of_element_located(self.INVITE_BTN))

    @allure.step("Пригласить сотрудника по почте: {email}")
    def invite_employee(self, email):
        self.wait.until(EC.element_to_be_clickable(self.INVITE_BTN)).click()

        field = self.wait.until(EC.visibility_of_element_located(self.EMAILS_INPUT))
        field.send_keys(email)

        # пробел после адреса превращает его в «чип» и включает кнопку
        field.send_keys(Keys.SPACE)

        # ждём, пока кнопка «Пригласить сотрудников» станет активной
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN_ENABLED)).click()

    @allure.step("Проверить уведомление об успешном приглашении")
    def is_invite_success_shown(self):
        return self.wait.until(EC.visibility_of_element_located(self.INVITE_TOAST)).is_displayed()

    @allure.step("Проверить, что сотрудник {email} есть в списке компании")
    def is_employee_in_list(self, email):
        return self._visible_employee_element(email).is_displayed()

    def has_employee(self, email):
        """Есть ли сотрудник в списке прямо сейчас (без ожидания)."""
        return len(self.driver.find_elements(*self._employee_row(email))) > 0

    @allure.step("Удалить сотрудника {email} из компании")
    def delete_employee(self, email):
        self._visible_employee_element(email).click()
        self.wait.until(EC.element_to_be_clickable(self.REMOVE_LINK)).click()
        self.wait.until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BTN)).click()
        self.wait.until(EC.visibility_of_element_located(self._deleted_message(email)))
        self.wait.until(EC.element_to_be_clickable(self.BACK_TO_COMPANY_BTN)).click()
