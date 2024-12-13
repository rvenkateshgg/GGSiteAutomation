import pytest
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from Utilities.report_utilities import get_report
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium.common import exceptions
import time

s = Service(executable_path="../../drivers/chromedriver")
site = "https://shop.greatergoods.com/collections/the-new-the-exciting-the-good/products/cold-press-juicer-1"
base_url = "https://shop.greatergoods.com"
path = '../Reports/brokenlink2.csv'


def pytest_addOption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run tests in headless mode"
    )


class TestBrokenLink:
    @pytest.fixture()
    def setup(self, request):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=s)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        yield
        self.driver.close()
        self.driver.quit()

    def test_broken_link(self, setup):
        self.driver.get(site)
        time.sleep(3)
        results = []
        All_links = self.driver.find_elements(By.TAG_NAME, "a")
        print(f"Total num of links: {len(All_links)}")
        urls = set(link.get_attribute("href") for link in All_links if link.get_attribute("href"))
        for url in urls:
            print(url)
            try:
                response = requests.get(url)
                if response.status_code >= 400:
                    print(f"Broken link: {url} status code: {response.status_code}")
                    results.append((url, response.status_code))
                    if results:
                        df = pd.DataFrame(results, columns=['Broken Link', 'Status code'])
                        df.to_csv(path, index=False)
                    else:
                        print("No Broken links found")
            except requests.RequestException as e:
                print(f"Error accessing {url}: {e}")

