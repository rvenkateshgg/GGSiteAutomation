import time

from Configurations.config import AppConfig
from Pages.gg_shopify.broken_link import GGShopifyBrokenLink
from TestCases.shared.conftest import webdriver_instance


class TestBrokenLink:

    def test_broken_link_main(self, webdriver_instance):
        checkedUrls = []  # List to keep track of checked URLs
        brokenUrls = []   # List to store broken URLs
        gg_shopify_broken_link = GGShopifyBrokenLink()  # Instantiate the class
        gg_shopify_broken_link.test_broken_link(webdriver_instance, AppConfig.GG_SHOPIFY.SITE_URL, checkedUrls, brokenUrls)
        time.sleep(5)

