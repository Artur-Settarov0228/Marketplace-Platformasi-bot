import requests
from config import API_BASE_URL


def telegram_login(payload):
    url = f"{API_BASE_URL}/auth/telegram-login/"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()

    return None