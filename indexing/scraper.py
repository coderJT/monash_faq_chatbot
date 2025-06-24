from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import time

start_time = time.time()

MONASH_STUDENT_ADMIN_URL = 'https://www.monash.edu/students/admin/dates/principal-dates'

### Source URLs scraping logic ###
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(MONASH_STUDENT_ADMIN_URL)

    # Accept cookies if present
    try:
        page.click('text="Accept all"', timeout=3000)
    except:
        pass

    page.wait_for_timeout(3000)  # Wait for content to render

    # Expand all sidebar buttons
    expand_buttons = page.query_selector_all('button.lhs-nav-list__item-cta')

    # Extract HTML after expansion
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    # Get all nested sidebar <li> items (level 3)
    categories = soup.find_all("li", class_="lhs-nav-list__item--lvl3")
    links = []  

    # Extract all sublinks (level 4 and 5) for each category (level 3)
    for category in categories:
        a_tags = category.find_all('a', class_="lhs-nav-list__item-link")
        for a_tag in a_tags:
            title = a_tag.get_text(strip=True)

            # Clean numbering in front
            cleaned_title = re.sub(r"^\d+\.\s*", "", title)
            links.append((cleaned_title, a_tag["href"]))

    browser.close()

    for title, url in links:
        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(f"{title} → {url}\n")

end_time = time.time()
print(f"Scraper took {end_time - start_time:.2f} seconds to scrape all URLs.")

