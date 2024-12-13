import pytest
from Utilities.web_driver_utility import get_webdriver


@pytest.fixture
def webdriver_instance(request):
    """
    Pytest fixture to provide a WebDriver instance.

    :param request: Pytest fixture to access command-line arguments.
    :return: WebDriver instance.
    """
    driver = get_webdriver()
    yield driver
    driver.quit()
