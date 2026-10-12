import requests

from config.config import BASE_URL


def test_get_projects_without_token() -> None:
    response = requests.get(
        f"{BASE_URL}/projects",
        timeout=10,
    )

    assert response.status_code == 401
    assert "Unauthorized" in response.text
