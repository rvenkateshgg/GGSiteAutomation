import pandas as pd
import requests
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

visited_links = set()


class GGShopifyBrokenLink:
    path = '../Reports/brokenlinks1.csv'

    def test_broken_link(self, webdriver_instance, input_url, checkedUrls, brokenUrls):
        print(f"Checking: {input_url}")

        try:
            # Check if the link is broken using requests
            response = requests.get(input_url)
            if response.status_code >= 400:
                print(f"Broken link: {input_url} status code: {response.status_code}")
                brokenUrls.append((input_url, response.status_code))
                # Save broken links to a CSV file
                if brokenUrls:
                    df = pd.DataFrame(brokenUrls, columns=["URL", "Status Code"])
                    df.to_csv(self.path, index=False)
                    send_file_to_slack(self.path)
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {input_url}: {e}")

        # Add the checked URL to the list
        checkedUrls.append(input_url)
        webdriver_instance.get(input_url)

        # Find all links on the page
        All_links = webdriver_instance.find_elements(By.TAG_NAME, "a")
        print(f"Total num of links in {input_url} : {len(All_links)}")

        # Get unique URLs (skip empty hrefs)
        urls = set(link.get_attribute("href") for link in All_links if link.get_attribute("href"))

        # Check each link recursively (if it's not checked yet and is on the same domain)
        for url in urls:
            if url.startswith("https://shop.greatergoods.com/") and url not in checkedUrls:
                try:
                    # Recursively check for broken links
                    self.test_broken_link(webdriver_instance, url, checkedUrls, brokenUrls)
                except StaleElementReferenceException:
                    pass
