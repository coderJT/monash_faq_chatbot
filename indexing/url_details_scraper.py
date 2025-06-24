import csv
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup, Comment
import os
import asyncio
import aiofiles
import time

start_time = time.time()

# Load all links from the CSV
links = []
with open("links.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.append((row["Title"], row["URL"]))

os.makedirs("pages", exist_ok=True)

async def scrape_page(browser, title, url):
    
    context = await browser.new_context()
    page = await context.new_page()
    current_index = links.index((title, url)) + 1
    total_links = len(links)
    print(f"Scraping ({current_index}/{total_links}): {title} - {url}")

    # For simplicity, we will disregard pdf files first
    if url.lower().endswith(".pdf"):
        print(f"Skipping PDF: {url}")
        return
    
    try:
        await page.goto(url, timeout=15000)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        await page.close()
        return

    try:
        await page.click('text="Accept all"', timeout=2000)
    except:
        pass

    # Resort to manual scraping
    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    raw_html = soup.find("div", class_="content-inner__main")
    if not raw_html:
        await page.close()
        return

    for tag in raw_html.find_all(["nav", "style", "script", "noscript", "iframe"]):
        tag.decompose()

    faq_help_panel = raw_html.find("div", id="monash-faq-help-panel")
    if faq_help_panel:
        faq_help_panel.decompose()

    for comment in raw_html.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    response = str(raw_html)

    async with aiofiles.open(f"pages/{title}.txt", "w", encoding="utf-8") as out:
        await out.write(response)

    await page.close()
    await context.close()

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()

        # Limit concurrency to avoid overloading system or being blocked
        semaphore = asyncio.Semaphore(5)

        async def sem_scrape(title, url):
            async with semaphore:
                await scrape_page(browser, title, url)

        tasks = [sem_scrape(title, url) for title, url in links]
        await asyncio.gather(*tasks)
        await browser.close()

        end_time = time.time()
        print(f"Scraper took {end_time - start_time:.2f} seconds to scrape all URL's information.")

asyncio.run(main())