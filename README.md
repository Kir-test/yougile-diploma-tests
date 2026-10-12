# yougile-diploma-tests

Автоматизированное тестирование YouGile (API и UI) — дипломный проект.

## О проекте

Проект предназначен для автоматизированной проверки функциональности API
и пользовательского интерфейса системы управления проектами YouGile.

## Технологии

- Python 3.13
- pytest
- Selenium WebDriver
- requests
- Allure Report

## Структура проекта

- `api_tests/` — API-тесты
- `ui_tests/` — UI-тесты (Selenium)
- `ui_tests/pages/` — Page Object Model
- `config/` — конфигурация тестов
- `screenshots/` — скриншоты шагов (для диплома)
- `requirements.txt` — зависимости
- `pytest.ini` — настройки pytest

## Установка

```bash
git clone https://github.com/Kir-test/yougile-diploma-tests.git
cd yougile-diploma-tests

python -m venv .venv
.venv\Scripts\activate       # Windows

pip install -r requirements.txt

Создай config/.env по образцу config/.env.example и заполни:
UI_BASE_URL=...
UI_EMAIL=...
UI_PASSWORD=...

Запуск тестов
# Все тесты
pytest --alluredir=allure-results

# Только UI
pytest ui_tests --alluredir=allure-results

# Только API
pytest api_tests --alluredir=allure-results

# Один файл
pytest ui_tests/test_invite_employee.py --alluredir=allure-results -v

Allure-отчёт
allure generate allure-results -o allure-report --clean
allure open allure-report

Или быстрый просмотр без генерации:
allure serve allure-results

Покрытые сценарии (UI)
Отображение формы авторизации

Успешный вход в YouGile

Открытие формы создания проекта

Отображение кнопки создания проекта после входа

Создание задачи в колонке «В работе»

Приглашение сотрудника в компанию по почте (с шагами и скриншотами в Allure)

Автор
Маевский Кирилл Викторович 
