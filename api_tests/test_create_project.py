import requests

from config.config import API_TOKEN, BASE_URL


def test_create_project() -> None:
    response = requests.post(
        f"{BASE_URL}/projects",
        headers={"Authorization": API_TOKEN.strip()},
        json={"title": "Автотестовый проект"},
        timeout=10,
    )

    assert response.status_code == 201

    data = response.json()
    assert "id" in data
    assert data["id"]
