from playwright.sync_api import sync_playwright

def scrape_circle(email, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.360neurogo.com/")
        page.fill('input[name="email"]', email)
        page.fill('input[name="password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')

        # Example: scrape dashboard content
        page.goto("https://www.360neurogo.com/dashboard")
        content = page.content()
        browser.close()
        return content
