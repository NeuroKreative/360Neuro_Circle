from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_circle(email, password, max_pages=30):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    collected_text = []
    visited_urls = set()
    to_visit = ["https://www.360neurogo.com/dashboard"]

    # Login
    driver.get("https://www.360neurogo.com/login")
    time.sleep(2)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]").click()
    time.sleep(3)

    while to_visit and len(visited_urls) < max_pages:
        url = to_visit.pop(0)
        if url in visited_urls:
            continue

        try:
            driver.get(url)
            time.sleep(2)
            page_text = driver.find_element(By.TAG_NAME, "body").text
            collected_text.append(f"--- {url} ---\n{page_text}")
            visited_urls.add(url)

            # Collect internal links
            links = driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                href = link.get_attribute("href")
                if href and "360neurogo.com" in href and "logout" not in href:
                    clean_href = href.split("?")[0]
                    if clean_href not in visited_urls and clean_href not in to_visit:
                        to_visit.append(clean_href)

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    driver.quit()
    return "\n\n".join(collected_text)


