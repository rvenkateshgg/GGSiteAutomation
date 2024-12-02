import pytest
import pandas as pd
import requests
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

s = Service(executable_path="../drivers/chromedriver")


class TestBrokenLink:
    @pytest.fixture()
    def setup(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--remote-allow-origins=*")
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        yield
        self.driver.close()
        self.driver.quit()

    def test_broken_link_main(self, setup):
        checkedUrls = []
        brokenUrls = []
        self.__test_broken_link(self, "https://shop.greatergoods.com/", checkedUrls, brokenUrls)

        if brokenUrls:
            columns = ['URL', 'Status code']
            df = pd.DataFrame(brokenUrls, columns=columns)
            df.to_csv('../Reports/brokenlinks10.csv', index=False)

    def __test_broken_link(self, setup, input_url, checkedUrls, brokenUrls):
        try:
            response = requests.get(input_url)
            if response.status_code == 200:
                print(f"Broken link: {input_url} status code: {response.status_code}")
                brokenUrls.append((input_url, response.status_code))
                return
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {input_url}: {e}")

        checkedUrls.append(input_url)
        self.driver.get(input_url)

        All_links = self.driver.find_elements(By.TAG_NAME, "a")
        print(f"Total num of links in {input_url} : {len(All_links)}")
        urls = set(link.get_attribute("href") for link in All_links if link.get_attribute("href"))

        for url in urls.copy():
            if url.startswith("https://shop.greatergoods.com/") and url not in checkedUrls:
                try:
                    brokenUrls.append(self.__test_broken_link(self, url, checkedUrls, brokenUrls))
                except StaleElementReferenceException:
                    pass

