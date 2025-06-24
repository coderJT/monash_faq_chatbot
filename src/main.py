from source_urls_scraper import scrape_url
from url_details_scraper import scrape_pages
from clean_scraped_result import process_data
from build_index import indexing
from query_rag import evaluate

async def main():

    # Step 1: Scrape source URLs
    urls = await scrape_url()

    # Step 2: Scrape details from URLs
    pages_data = await scrape_pages()

    # Step 3: Clean and process scraped data
    processed_data = process_data()

    # Step 4: Build index
    index = indexing()

    # Step 5: Launch the LLM
    answer = evaluate()

if __name__ == "__main__":
    main()