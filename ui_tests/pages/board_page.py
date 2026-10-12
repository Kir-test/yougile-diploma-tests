import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BoardPage:
    LEFT_SIDEBAR = '//*[@data-testid="left-sidebar"]'
    BOARD_COLUMN = '//*[@data-testid="board-column"]'

    ADD_TASK_BTN = (By.CSS_SELECTOR, '[data-testid="link-button-new"]')
    TASK_NAME_INPUT = (By.CSS_SELECTOR, '[data-testid="board-task-input-name"]')

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Открыть проект «{name}» в сайдбаре")
    def open_project(self, name):
        locator = (By.XPATH, f'{self.LEFT_SIDEBAR}//*[text()="{name}"]')
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step("Проверить, что открыта доска «{name}»")
    def wait_board_opened(self, name):
        locator = (By.XPATH, f'//*[text()="{name}"]')
        self.wait.until(EC.visibility_of_element_located(locator))

    def get_column(self, title):
        """Колонка по названию: ищем board-column, внутри которой есть заголовок."""
        locator = (By.XPATH, f'{self.BOARD_COLUMN}[.//span[text()="{title}"]]')
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Создать задачу «{task_title}» в колонке «{column_title}»")
    def create_task(self, column_title, task_title):
        column = self.get_column(column_title)
        column.find_element(*self.ADD_TASK_BTN).click()

        task_input = self.wait.until(
            lambda d: column.find_element(*self.TASK_NAME_INPUT)
        )
        task_input.send_keys(task_title)
        # Enter сохраняет задачу (после этого открывается поле для следующей)
        task_input.send_keys(Keys.ENTER)

    @allure.step("Проверить, что задача «{task_title}» есть в колонке «{column_title}»")
    def is_task_in_column(self, column_title, task_title):
        column = self.get_column(column_title)
        # текст заголовка может быть разбит на вложенные span, поэтому берём normalize-space(.)
        card_title = (
            By.XPATH,
            f'.//*[@data-testid="tw-task-container"]'
            f'//*[@data-testid="board-task-title"][normalize-space(.)="{task_title}"]',
        )
        card = self.wait.until(lambda d: column.find_element(*card_title))
        return card.is_displayed()
