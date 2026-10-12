import requests

from config.config import API_TOKEN, BASE_URL


def test_get_tasks() -> None:
    response = requests.get(
        f"{BASE_URL}/tasks",
        headers={"Authorization": API_TOKEN.strip()},
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
