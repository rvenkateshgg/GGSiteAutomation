import time
import pytest
from selenium import webdriver
import time

from Configurations.config import AppConfig
from Pages.gg_shopify.find_broken_link import FindBrokenLink
from TestCases.shared.conftest import webdriver_instance


class TestBrokenLink:

    def test_broken_link_main(self, webdriver_instance):
        webdriver_instance.get(AppConfig.GG_SHOPIFY.SITE_URL)
        self.broken_link = FindBrokenLink()
        self.broken_link.is_valid_url(AppConfig.GG_SHOPIFY.SITE_URL)
        self.broken_link.check_link(AppConfig.GG_SHOPIFY.SITE_URL, AppConfig.GG_SHOPIFY.SITE_URL)
        self.broken_link.find_and_check_links(AppConfig.GG_SHOPIFY.SITE_URL, AppConfig.GG_SHOPIFY.SITE_URL)
