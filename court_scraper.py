from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def fetch_case_table():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible browser
        page = browser.new_page()

        # Open Delhi High Court Case Status page
        page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)

        print("🔹 Fill details + Solve Captcha + Click Submit")
        print("🔹 Table load hone ka wait kar rahe hain...")

        # Wait for the table to appear
        try:
            page.wait_for_selector("table", timeout=120000)  # 2 min wait
        except:
            browser.close()
            return {"error": "Table did not appear. Maybe captcha failed."}

        # Wait a little for safety
        time.sleep(2)

        html = page.content()
        browser.close()

    # Parse HTML to extract only the table
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return {"error": "No table found on page"}

    # Return the table HTML
    return {"table_html": str(table)}
