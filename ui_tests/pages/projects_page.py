
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ProjectsPage:
    ADD_PROJECT_BUTTON = (
        By.CSS_SELECTOR,
        '[data-testid="add-project-button"]',
    )
    PROJECT_WITH_TASKS_OPTION = (
        By.XPATH,
        '//*[normalize-space()="Проект с задачами"]',
    )
    NEW_PROJECT_MODAL_TITLE = (
        By.XPATH,
        '//*[normalize-space()="Новый проект с задачами"]',
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_add_project_button_visible(self) -> bool:
        button = self.wait.until(
            EC.visibility_of_element_located(
                self.ADD_PROJECT_BUTTON
            )
        )
        return button.is_displayed()

    def open_project_creation_modal(self) -> None:
        add_button = self.wait.until(
            EC.element_to_be_clickable(
                self.ADD_PROJECT_BUTTON
            )
        )
        add_button.click()

        project_option = self.wait.until(
            EC.element_to_be_clickable(
                self.PROJECT_WITH_TASKS_OPTION
            )
        )
        project_option.click()

    def is_project_creation_modal_visible(self) -> bool:
        title = self.wait.until(
            EC.visibility_of_element_located(
                self.NEW_PROJECT_MODAL_TITLE
            )
        )
        return title.is_displayed()
