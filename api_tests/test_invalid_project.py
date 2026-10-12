import requests

from config.config import API_TOKEN, BASE_URL


def test_create_project_with_empty_title() -> None:
    response = requests.post(
        f"{BASE_URL}/projects",
        headers={"Authorization": API_TOKEN.strip()},
        json={"title": ""},
        timeout=10,
    )

    assert response.status_code == 400
    assert "title should not be empty" in response.text
