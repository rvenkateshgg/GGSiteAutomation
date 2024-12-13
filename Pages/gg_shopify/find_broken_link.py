import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from Configurations.config import AppConfig
from Configurations.report_config import ReportConfig
from Utilities.report_utilities import get_report
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd

from Utilities.slackUtils import SendFile

# Store visited links to avoid redundant checks
visited_links = set()
results = []


class FindBrokenLink:
    @staticmethod
    def is_valid_url(url):
        """Check if the URL is valid and absolute."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    @staticmethod
    def check_link(url, parenturl):
        """Check if the URL is reachable."""
        try:
            response = requests.get(url, timeout=5)
            if response.status_code >= 400:
                print(f"Broken link: {url} (Status code: {response.status_code}) - Found on: {parenturl}")
                results.append((url, response.status_code, parenturl))
                if results:
                    df = pd.DataFrame(results, columns=["URL", "Status Code", "Parent url"])
                    df.to_csv(AppConfig.REPORT, index=False)
                return False
            else:
                print(f"Valid link: {url}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Broken link: {url} (Error: {e}) - Found on:{parenturl}")
            return False

    @staticmethod
    def find_and_check_links(base_url, url, parent_url=None):
        """Find and check all links on the page."""
        if url in visited_links:
            return
        visited_links.add(url)
        try:
            response = requests.get(url, timeout=5)
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
            except:
                soup = BeautifulSoup(response.content, 'lxml')
            for link in soup.find_all('a', href=True):
                link_url = urljoin(base_url, link['href'])  # Resolve relative URLs
                if FindBrokenLink.is_valid_url(link_url) and urlparse(link_url).netloc == urlparse(base_url).netloc:
                    if link_url not in visited_links:
                        FindBrokenLink.check_link(link_url, url)
                        FindBrokenLink.find_and_check_links(base_url, link_url, parent_url=url)  # Recursively crawl
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {url} (Error: {e})")
