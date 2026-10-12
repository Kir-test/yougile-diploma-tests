import uuid

import allure

from ui_tests.pages.board_page import BoardPage


@allure.epic("Yougile")
@allure.feature("Задачи")
@allure.title("Создание задачи в колонке «В работе»")
@allure.severity(allure.severity_level.CRITICAL)
def test_task_is_created_in_in_progress_column(logged_in_driver) -> None:
    task_title = f"Автотест {uuid.uuid4().hex[:8]}"

    board = BoardPage(logged_in_driver)
    board.open_project("Учебный")
    board.wait_board_opened("Моя доска")

    board.create_task("В работе", task_title)

    assert board.is_task_in_column("В работе", task_title), (
        f"Задача «{task_title}» не появилась в колонке «В работе»"
    )
