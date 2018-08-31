import sys
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

BROWSER = None
TIME_DEFAULT = 5

LOG = logging.getLogger('Kickstarter_Search_Service')
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level = logging.INFO, format = FORMAT)

DELAYS = {'page_load': 3, 'search_load': 4, 'ajax_load': 2}

def init_browser(headless = False):
    options = Options()
    options.set_headless(headless = headless)
    BROWSER = webdriver.Firefox(firefox_options = options)
    BROWSER.set_window_size(800, 750)
    LOG.info("Running the Browser.")
    return BROWSER

def get_kickstarter_page(BROWSER):
    BROWSER.get("https://www.kickstarter.com/")
    assert "Kickstarter" in BROWSER.title

    LOG.info("Waiting for the page to load all elements")
    time.sleep(DELAYS.get("page_load", TIME_DEFAULT))
    LOG.info("Done")

def search(BROWSER):
    search_elem = BROWSER.find_element(By.XPATH, '//button/span[text()="Search"]')
    ActionChains(BROWSER).move_to_element(search_elem).click().send_keys('DIY Electronics').perform()

    LOG.info("Waiting for the page to load search results")
    time.sleep(DELAYS.get("search_load", TIME_DEFAULT))
    LOG.info("Done")

    categories_elem = BROWSER.find_element(By.XPATH, '//div/span[text()="All"]')
    categories_elem.click()
    
    LOG.info("Waiting for the page to load Categories")
    time.sleep(DELAYS.get("page_load", TIME_DEFAULT))
    LOG.info("Done")

    more_filters_elem = BROWSER.find_element(By.XPATH, '//*[@id="filters"]')
    more_filters_elem.click()

    LOG.info("Waiting for ajax element to load more filters")
    time.sleep(DELAYS.get("ajax_load", TIME_DEFAULT))
    LOG.info("Done")

    #filter_project_elem = BROWSER.find_element(By.XPATH, '//span/span[text()="All projects"]')
    #ActionChains(BROWSER).move_to_element(filter_project_elem).click().perform()

    successful_proj_elem = BROWSER.find_element(By.XPATH, '//select[@name="state"]/option[text()="Successful projects"]')
    successful_proj_elem.click()

    LOG.info("Waiting for ajax element to load page with the selected option")
    time.sleep(DELAYS.get("page_load", TIME_DEFAULT))
    LOG.info("Done")

    more_filters_elem.click()
    time.sleep(2)

    sort_by_element = BROWSER.find_element(By.XPATH, '//span[text()="Magic"]')
    sort_by_element.click()
    time.sleep(2)

    sort_by_date_elem = BROWSER.find_element(By.XPATH, '//li[@data-sort="end_date"]')
    sort_by_date_elem.click()

if __name__ == '__main__':
    LOG.info("Running the Script")
    browser = init_browser()
    LOG.info(browser)
    if not browser:
        LOG.error("Unable to initialize Browser.")
        sys.exit()
    get_kickstarter_page(browser)
    search(browser)
