import requests
from bs4 import BeautifulSoup
import time

def scrape_circle(api_key, start_urls, max_pages=30):
    visited_urls = set()
    to_visit = list(start_urls)
    collected_text = []

    while to_visit and len(visited_urls) < max_pages:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        try:
            response = requests.get(
                "https://app.scrapingbee.com/api/v1/",
                params={
                    "api_key": api_key,
                    "url": url,
                    "render_js": "true"
                }
            )
            soup = BeautifulSoup(response.text, "html.parser")
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



