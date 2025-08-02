from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_case_data(case_type, case_number, case_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Step 1: Open Delhi HC case status page
        page.goto("https://delhihighcourt.nic.in/app/get-case-type-status", timeout=60000)

        # Step 2: Fill form
        page.select_option("select[name='case_type']", case_type)
        page.fill("input[name='case_no']", case_number)
        page.fill("input[name='case_year']", case_year)

        print("\n🔹 Solve captcha manually & click Submit")
        print("🔹 Waiting for hearing details table...")

        # Step 3: Wait for result table (2 min max)
        try:
            page.wait_for_selector("table", timeout=120000)
        except:
            print("❌ Table did not load (captcha fail or wrong case)")
            browser.close()
            return {"error": "No data found or captcha failed"}

        html = page.content()
        browser.close()

    # Step 4: Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return {"error": "No table found on page"}

    # Extract headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    rows_data = []

    # Extract each row
    for row in table.find_all("tr")[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            rows_data.append(dict(zip(headers, cols)))

    return {"headers": headers, "rows": rows_data}
