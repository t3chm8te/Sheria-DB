import os
import re
import requests
import logging
import time

from urllib.parse import urljoin
from bs4 import BeautifulSoup

log_directory = "../logs"
os.makedirs(log_directory, exist_ok=True)

# Configure logging
log_file = os.path.join(log_directory, "Gazette_Crawler.log")  # Store log in logs/crawler.log
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # Log INFO and higher levels
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Add console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

class GazetteCrawler:
    def __init__(self, base_url: str = "https://new.kenyalaw.org/", gazettes_url: str = "https://new.kenyalaw.org/gazettes/"):
        self.base_url = base_url
        self.gazettes_url = gazettes_url
        self.visited_urls = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

    def get_available_years(self):
        """Fetch the main page and extract available years dynamically"""

        logging.info(f"Fetching available years from {self.gazettes_url}")

        response = requests.get(self.gazettes_url)
        if response.status_code != 200:
            logging.error(f"Failed to fetch main gazette page: {self.gazettes_url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        
        target_div = soup.find("div", class_="row mt-5")
        
        full_urls = []
        pattern = re.compile(r"^/gazettes/(\d{4})$")

        for link in target_div.find_all("a", href=True):
            match = pattern.match(link["href"])
            if match:
                full_url = urljoin(self.gazettes_url, link["href"])
                full_urls.append(full_url)

        logging.info(f"Extracted year links: {full_urls}")
        return sorted(set(full_urls), reverse=True)

    def get_available_gazettes(self, year_url): # Gets links to gazzettes for every year
        if year_url in self.visited_urls:
            logging.info(f"Skipping already visited URL: {year_url}")
            return []
        
        logging.info(f"Crawling year page: {year_url}")
        self.visited_urls.add(year_url)  # Mark as visited

        response = requests.get(year_url)
        if response.status_code != 200:
            logging.error(f"Failed to fetch: {year_url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        target_table = soup.find(id="doc-table")
        if not target_table:
            logging.warning(f"No document table found in {year_url}, skipping.")
            return []

        links = []

        # Extract all links inside the year page
        for link in target_table.find_all("a", href=True):
            gazette_url = urljoin(self.base_url, link["href"])
            if gazette_url not in self.visited_urls:  # Avoid revisiting
                links.append(gazette_url)

        return links

    def download_pdfs(self, year, gazette_links, download_directory="../Dataset/Gazettes"):
        """Download PDF files from the extracted links"""
        year_download_dir = os.path.join(download_directory, year)
        os.makedirs(year_download_dir, exist_ok=True)

        for gazette_url in gazette_links:
            pdf_url = f"{gazette_url}/source"
            file_name = os.path.join(year_download_dir, pdf_url.split("/")[-2] + ".pdf")

            if os.path.exists(file_name):
                logging.info(f"File already exists: {file_name}, skipping.")
                continue

            logging.info(f"Downloading: {pdf_url}")
            response = requests.get(pdf_url, headers=self.headers, stream=True)
            time.sleep(5)  # Respect crawl delay

            if response.status_code == 200:
                with open(file_name, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)
                logging.info(f"Saved: {file_name}")
            else:
                logging.error(f"Failed to download: {pdf_url}")

    def start_crawl(self):
        """Start the crawling process."""
        logging.info("Starting crawl...")
        year_links = self.get_available_years()

        for year_link in year_links:
            year = year_link.split('/')[-1]  
            gazette_links = self.get_available_gazettes(year_link)
            logging.info(f"Finished crawling {year_link}, found {len(gazette_links)} gazettes.")
            self.download_pdfs(year, gazette_links)

if __name__ == "__main__":
    crawler = GazetteCrawler()
    crawler.start_crawl()