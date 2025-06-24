import csv
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup, Comment
import os
import asyncio
import aiofiles

# Load all links from the CSV
links = []
with open("links.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.append((row["Title"], row["URL"]))

os.makedirs("pages", exist_ok=True)

async def scrape_page(browser, title, url):
    page = await browser.new_page()
    print(f"Scraping: {title} - {url}")
    await page.goto(url)

    try:
        await page.click('text="Accept all"', timeout=2000)
    except:
        pass

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

    cleaned_html = str(raw_html)

    async with aiofiles.open(f"pages/{title}.txt", "w", encoding="utf-8") as out:
        await out.write(cleaned_html)

    await page.close()

async def main():
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch()

        # Limit concurrency to avoid overloading system or being blocked
        semaphore = asyncio.Semaphore(10)

        async def sem_scrape(title, url):
            async with semaphore:
                await scrape_page(browser, title, url)

        tasks = [sem_scrape(title, url) for title, url in links]
        await asyncio.gather(*tasks)
        await browser.close()

asyncio.run(main())