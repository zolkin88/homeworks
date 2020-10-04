import pytest
from selenium import webdriver
from selenium.webdriver import FirefoxOptions, ChromeOptions


def pytest_addoption(parser):
    parser.addoption("--browser", default="firefox")
    parser.addoption("--base_url", default="http://localhost")
    parser.addoption("--path", default="/admin")


@pytest.fixture
def get_base_url(request):
    base_url = request.config.getoption("--base_url")
    return base_url


@pytest.fixture
def get_path(request):
    path = request.config.getoption("--path")
    return path


@pytest.fixture
def browser(request, get_base_url, get_path):
    if "chrome" == request.config.getoption("--browser"):
        chrome_options = ChromeOptions
        chrome_options.headless = True
        driver = webdriver.Chrome(executable_path='./chromedriver')
        driver.maximize_window()
    else:
        firefox_options = FirefoxOptions()
        firefox_options.headless = False
        driver = webdriver.Firefox(executable_path='./geckodriver',
                                   options=firefox_options)
        driver.maximize_window()

    def open(path=get_path):
        return driver.get(get_base_url + path)
    driver.open = open
    driver.open()
    yield driver
    driver.quit()
