import requests
from bs4 import BeautifulSoup

def scrape_circle(email, password):
    session = requests.Session()

    # Step 1: Get login page (to grab CSRF token if needed)
    login_page = session.get("https://www.360neurogo.com/login")
    soup = BeautifulSoup(login_page.text, "html.parser")

    # Optional: Extract CSRF token if required
    # csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

    # Step 2: Submit login form
    payload = {
        "email": email,
        "password": password,
        # "csrf_token": csrf_token  # Include if needed
    }
    response = session.post("https://www.360neurogo.com/login", data=payload)

    # Step 3: Access protected page
    dashboard = session.get("https://www.360neurogo.com/dashboard")
    return dashboard.text

