from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse
import os
from bs4 import BeautifulSoup


class MyCrawlSpider(CrawlSpider):
    name = "norse_spider"
    allowed_domains = ["norse-mythology.org"]  # Replace with target domain
    start_urls = ["https://norse-mythology.org/"]  # Replace with your base URL

    rules = (
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        parsed_url = urlparse(response.url)

        # Extract the path and convert it into a folder structure
        path_parts = parsed_url.path.strip("/").split("/")
        if not path_parts or path_parts == [""]:
            path_parts = ["index"]  # Default for the homepage

        # Construct the directory path
        # Exclude last part for filename
        save_dir = os.path.join("crawled_pages", *path_parts[:-1])
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

        # Define the file name (last part of the URL or 'index' if empty)
        page_name = path_parts[-1] if path_parts[-1] else "index"

        # Save to html format
        # file_name = f"{page_name}.html"
        # file_path = os.path.join(save_dir, file_name)
        # with open(file_path, "wb") as f:
        #     f.write(response.body)

        # Save to txt format
        file_name = f"{page_name}.txt"
        file_path = os.path.join(save_dir, file_name)
        soup = BeautifulSoup(response.text, 'html.parser')
        title_text = soup.title.string.strip() if soup.title else ''
        p_texts = '\n'.join(p.get_text(separator=' ', strip=True)
                            for p in soup.find_all('p'))
        extracted_text = f"{title_text}\n{p_texts}" if title_text else p_texts
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        self.log(f"Saved file {file_path}")
