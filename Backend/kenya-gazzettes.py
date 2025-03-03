import requests
from bs4 import BeautifulSoup

class GazetteScraper:
    def __init__(self, base_url: str = "https://new.kenyalaw.org/gazettes/"):
        self.base_url = base_url

    def get_available_years(self):
        """Fetch the main page and extract available years dynamically"""
        response = requests.get(self.base_url)
        if response.status_code != 200:
            print("Failed to fetch the main gazette page")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        years = []

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.strip("/").isdigit():  # Check if it's a year (e.g., "2024/")
                years.append(href.strip("/"))

        return sorted(set(years), reverse=True)  # Return unique years in descending order

    def get_gazettes_for_year(self, year: str):
        """Fetch all gazette file links for a given year"""
        year_url = f"{self.base_url}{year}/"
        response = requests.get(year_url)
        if response.status_code != 200:
            print(f"Failed to fetch gazettes for {year}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        gazettes = []

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.endswith(".pdf"):  # Assuming gazettes are PDF files
                full_url = year_url + href
                gazettes.append(full_url)

        return gazettes

# Instantiate scraper
scraper = GazetteScraper()

# Get available years
years = scraper.get_available_years()
print(f"Available years: {years}")

# Get gazettes for a specific year
if years:
    gazettes_2024 = scraper.get_gazettes_for_year("2024")
    print(f"Gazettes for 2024: {gazettes_2024}")