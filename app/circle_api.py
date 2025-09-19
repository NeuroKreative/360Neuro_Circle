import requests
import os

CIRCLE_API_URL = "https://app.circle.so/api/v1"

def get_auth_token():
    email = os.getenv("CIRCLE_EMAIL")
    password = os.getenv("CIRCLE_PASSWORD")
    response = requests.post(f"{CIRCLE_API_URL}/auth/login", json={"email": email, "password": password})
    return response.json().get("token")

def fetch_posts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{CIRCLE_API_URL}/posts", headers=headers)
    return response.json()

def fetch_token(email, password):
    response = requests.post(f"{CIRCLE_API_URL}/auth/login", json={"email": email, "password": password})
    return response.json().get("token")
