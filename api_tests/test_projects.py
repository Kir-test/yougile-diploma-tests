import requests

from config.config import API_TOKEN, BASE_URL


def test_get_projects():
    response = requests.get(
        f"{BASE_URL}/projects",
        headers={"Authorization": API_TOKEN.strip()},
        timeout=10,
    )
    print(response.text)

    assert response.status_code == 200

    data = response.json()
    assert "content" in data
    assert isinstance(data["content"], list)
