import requests

BASE_URL = "http://localhost:8000"


def register_user(
    full_name,
    email,
    password
):
    return requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password
        },
        timeout=5
    )


def login_user(
    email,
    password
):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        },
        timeout=5
    )


def get_current_user(
    token
):
    return requests.get(
        f"{BASE_URL}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        },
        timeout=5
    )