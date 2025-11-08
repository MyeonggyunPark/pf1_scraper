# --- Standard library imports ---
import time                                             # For adding delays between page loads
from abc import ABC, abstractmethod                     # For creating abstract base classes

# --- Third-party library imports ---
import requests                                         # For sending HTTP requests to websites
from bs4 import BeautifulSoup                           # For parsing and extracting data from HTML
from selenium import webdriver                          # For automating browser interactions
from selenium.webdriver.chrome.options import Options   # For configuring Chrome browser settings


# Base configuration shared by all scraper subclasses
class JobScraper(ABC):

    def __init__(self):
        self.BASE_URL = ""
        self.USER_HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
        self.infos_list = []

    @abstractmethod
    def get_url(self, keyword):
        """Generate URL based on the given keyword"""
        pass

    def extract_text(self, tag):
        """Extract text from a single tag or return 'No Information' if missing"""
        return tag.get_text(strip=True) if tag else "No Information"

    def extract_link(self, tag):
        """Extract href attribute from an anchor tag"""
        return tag.get("href", "No Link") if tag else "No Link"

    @abstractmethod
    def get_infos(self, url):
        """Extract job information from each job listing"""
        pass

    def infos_print(self, infos):
        """Print collected job information in a clean format"""
        print("\n======= [📑 INFO] ======")
        for info in infos:
            print()
            for k, v in info.items():
                if isinstance(v, list):
                    print(f"[{k}] : {' / '.join(v)}")
                else:
                    print(f"[{k}] : {v}")

    @abstractmethod
    def run(self):
        """Run the entire scraping process"""


# Scraper for berlinstartupjobs.com
class BSJscraper(JobScraper):

    def __init__(self, base_url):
        super().__init__()
        self.BASE_URL = base_url
        self.COMPANY_LOCATION = "Berlin"

    def get_url(self, keyword):
        url = f"{self.BASE_URL}{keyword}/"
        return url

    def get_infos(self, url):

        response = requests.get(url, headers=self.USER_HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            jobs_list = soup.find_all("li", class_="bjs-jlid")

            for job in jobs_list:
                job_title_tag = job.find("h4", class_="bjs-jlid__h")
                company_name_tag = job.find("a", class_="bjs-jlid__b")
                job_link_tag = job_title_tag.find("a")

                infos = {
                    "job_title": self.extract_text(job_title_tag),
                    "company_name": self.extract_text(company_name_tag),
                    "company_location": self.COMPANY_LOCATION,
                    "job_link": self.extract_link(job_link_tag),
                }

                self.infos_list.append(infos)

            response.status_code
        else:
            response.status_code

    def run(self, keyword):
        self.infos_list = []
        url = self.get_url(keyword)
        self.get_infos(url)

        return self.infos_list


# Scraper for weworkremotely.com
class WWRscraper(JobScraper):

    def __init__(self, base_url):
        super().__init__()
        self.BASE_URL = base_url
        self.LINK_URL = "https://weworkremotely.com"

    def get_url(self, keyword):
        return f"{self.BASE_URL}{keyword}"

    # Use Selenium to render JS-based content
    def get_infos(self, url):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            # Wait for page to fully render
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        finally:
            # Ensure browser closes even on failure
            driver.quit()

        jobs_list = soup.find_all("li", class_="new-listing-container")

        for job in jobs_list:
            title_tag = job.find("h3", class_="new-listing__header__title")
            company_tag = job.find("p", class_="new-listing__company-name")
            location_tag = job.find("p", class_="new-listing__company-headquarters")
            link_tag = job.find("a", class_="listing-link--unlocked")

            infos = {
                "job_title": self.extract_text(title_tag),
                "company_name": self.extract_text(company_tag),
                "company_location": self.extract_text(location_tag),
                "job_link": f"{self.LINK_URL}{self.extract_link(link_tag)}",
            }

            self.infos_list.append(infos)

    def run(self, keyword):
        self.infos_list = []
        url = self.get_url(keyword)
        self.get_infos(url)

        return self.infos_list


# Scraper for stepstone.de
class SSDscraper(JobScraper):
    def __init__(self, base_url):
        super().__init__()
        self.BASE_URL = base_url
        self.LINK_URL = "https://www.stepstone.de"
        self.COMPANY_LOCATION = "Germany"

    # Split base URL at '?' to insert keyword dynamically
    def get_url(self, keyword):
        split_index = self.BASE_URL.index("?")
        prefix = self.BASE_URL[:split_index]
        query = self.BASE_URL[split_index:]
        return f"{prefix}{keyword}{query}"

    # Remove 'Home' or remote-related terms from location text
    def location_filter(self, text):
        parts = [part.strip() for part in text.split(",")]
        filtered = [p for p in parts if "Home" not in p]
        return ", ".join(filtered)

    def get_infos(self, url):

        response = requests.get(url, headers=self.USER_HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            jobs_list = soup.find_all("article", class_="res-4cwuay")

            for job in jobs_list:
                job_title_tag = job.find("div", class_="res-ewgtgq")
                company_name_tag = job.find("span", class_="res-du9bhi")

                row_location_tag = job.find("div", class_="res-12jlzgf")
                location_tag = row_location_tag.find("span", class_="res-du9bhi")

                job_link_tag = job.find("a", class_="res-1fudl87")

                infos = {
                    "job_title": self.extract_text(job_title_tag),
                    "company_name": self.extract_text(company_name_tag),
                    "company_location": f"{self.location_filter(self.extract_text(location_tag))} (in {self.COMPANY_LOCATION})",
                    "job_link": f"{self.LINK_URL}{self.extract_link(job_link_tag)}"
                }

                self.infos_list.append(infos)

            response.status_code
        else:
            response.status_code

    def run(self, keyword):
        self.infos_list = []
        url = self.get_url(keyword)
        self.get_infos(url)

        return self.infos_list


if __name__ == "__main__":

    scraper1 = BSJscraper("https://berlinstartupjobs.com/skill-areas/")
    scraper1.run("python")
    print(f"\n총 {len(scraper1.infos_list)}개 공고 수집됨")

    scraper2 = WWRscraper("https://weworkremotely.com/remote-jobs/search?term=")
    scraper2.run("python")
    print(f"\n총 {len(scraper2.infos_list)}개 공고 수집됨")

    scraper3 = SSDscraper(
        "https://www.stepstone.de/jobs/?page=1&searchOrigin=Homepage_top-search"
    )
    scraper3.run("javascript")
    print(f"\n총 {len(scraper3.infos_list)}개 공고 수집됨")
