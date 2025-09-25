import requests
from bs4 import BeautifulSoup
import time

def scrape_circle(email, password, max_pages=30):  # Increased depth
    session = requests.Session()

    # Step 1: Log in to Circle
    login_url = "https://www.360neurogo.com/login"
    dashboard_url = "https://www.360neurogo.com/dashboard"

    session.get(login_url)
    payload = {"email": email, "password": password}
    session.post(login_url, data=payload)

    # Step 2: Crawl from dashboard
    visited_urls = set()
    to_visit = [dashboard_url]
    collected_text = []

    while to_visit and len(visited_urls) < max_pages:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        try:
            response = session.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract visible text
            page_text = soup.get_text(separator="\n", strip=True)
            collected_text.append(f"--- {url} ---\n{page_text}")
            visited_urls.add(url)

            # Find internal links
            for link in soup.find_all("a", href=True):
                href = link["href"]
                if href.startswith("/") and "logout" not in href:
                    full_url = f"https://www.360neurogo.com{href.split('?')[0]}"
                    if full_url not in visited_urls and full_url not in to_visit:
                        to_visit.append(full_url)

            time.sleep(1)

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    return "\n\n".join(collected_text)

