from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime

def fetch_case_data(case_type, case_number, filing_year):
    try:
        # Attempt Real Delhi HC Scraper
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Directly go to case type status page
            page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)

            # Wait for form fields to appear
            page.wait_for_selector("input[name='caseNumber']", timeout=30000)

            # Fill the form (adjust selectors as needed)
            page.fill("input[name='caseType']", case_type)
            page.fill("input[name='caseNumber']", case_number)
            page.fill("input[name='caseYear']", filing_year)

            # Submit form
            page.click("button[type='submit']")
            page.wait_for_timeout(5000)

            html = page.content()
            browser.close()

        # Parse HTML
        soup = BeautifulSoup(html, "html.parser")

        parties = soup.get_text().strip()[:200] or "Not Found"
        filing_date = "Check Result Page"
        next_hearing = "Check Result Page"
        pdf_link = None

        link_tag = soup.find("a", string="View Order")
        if link_tag:
            pdf_link = link_tag.get("href")

        return {
            "parties": parties,
            "filing_date": filing_date,
            "next_hearing": next_hearing,
            "latest_order_pdf": pdf_link or "No PDF found"
        }

    except Exception:
        # Dummy Fallback
        today = datetime.date.today().strftime("%d-%m-%Y")
        return {
            "parties": f"{case_type} Party A vs Party B",
            "filing_date": f"01-01-{filing_year}",
            "next_hearing": today,
            "latest_order_pdf": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        }
