import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Load all links from the CSV
links = []
with open("links.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.append((row["Title"], row["URL"]))

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for title, url in links:
        print(f"Scraping: {title} - {url}")
        page.goto(url)

        try:
            page.click('text="Accept all"', timeout=2000)
        except:
            pass

        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        # Example: Get all paragraphs
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # Save or process the scraped data
        with open(f"pages/{title}.txt", "w", encoding="utf-8") as out:
            out.write(text)

    browser.close()
