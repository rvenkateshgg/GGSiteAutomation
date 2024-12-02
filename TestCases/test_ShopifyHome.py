import pytest
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from Configuration.Slack_api import SLACKAPI
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from selenium.common import exceptions
import time

s = Service(executable_path="../drivers/chromedriver")
site = "https://shop.greatergoods.com/"
base_url = "https://shop."
path = '../Reports/brokenlinks14.csv'


def pytest_addOption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run tests in headless mode"
    )


class TestBrokenLink:
    @pytest.fixture()
    def setup(self, request):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=s, options=options)
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
            if url.startswith(base_url):
                self.driver.get(url)
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        print(f"Broken link: {url} status code: {response.status_code}")
                        results.append(f"Broken link: {url}, status code: {response.status_code}")
                        break
                except requests.RequestException as e:
                    print(f"Error accessing {url}: {e}")
            else:
                print(f"Skipping invalid URL: {url}")
        if results:
            df = pd.DataFrame(results)
            df.to_csv(path, index=False)
            self.slack = SLACKAPI()
            self.slack.send_file_to_slack(path)
        else:
            print("No Broken links present")
