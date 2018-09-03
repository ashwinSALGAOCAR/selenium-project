import sys
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException

BROWSER = None
TIME_DEFAULT = 5

LOG = logging.getLogger('Kickstarter_Search_Service')
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level = logging.INFO, format = FORMAT)

DELAYS = {'page_load': 3, 'search_load': 4, 'ajax_load': 2, 'go_back_load': 2}

def init_browser(headless = False):
    options = Options()
    options.set_headless(headless = headless)
    BROWSER = webdriver.Firefox(firefox_options = options)
    #BROWSER.set_window_size(800, 750)
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

def explore_projects(BROWSER):
    total_proj_elem = BROWSER.find_element(By.XPATH, '//b[@class="count ksr-green-500"]')
    total_projects = total_proj_elem.text
    print "\nListing " + total_projects
    time.sleep(DELAYS.get("projects_load", TIME_DEFAULT))

def get_project_details(BROWSER):
    PROJECT_COUNT = 0
    proj_list_elem = BROWSER.find_elements(By.XPATH, '//a[@class="block img-placeholder w100p"]')
    for project in proj_list_elem:
        project_link =  project.get_attribute('href')
        PROJECT_COUNT+=1
        print "Project " + str(PROJECT_COUNT) + ":" + project_link

        windows_before  = BROWSER.current_window_handle
        BROWSER.execute_script('''window.open('', "project_link_blank");''')
        LOG.info("Opening New Tab")
        windows_after = BROWSER.window_handles
        new_window = [x for x in windows_after if x != windows_before][0]
        BROWSER.switch_to_window(new_window)
        BROWSER.get(project_link)
        time.sleep(DELAYS.get("project_load", TIME_DEFAULT))

        proj_title_elem = BROWSER.find_element(By.XPATH, '//a[@class="hero__link"]')
        print "Title: " + proj_title_elem.text
        proj_fund_elem = BROWSER.find_element(By.XPATH, '//h3/span[@class="money"]')
        print "Total Funding: " + proj_fund_elem.text
        proj_pledge_elem = BROWSER.find_element(By.XPATH, '//div[@class="type-12 medium navy-500"]/span[@class="money"]')
        print "Plegded of : " + proj_pledge_elem.text + " goal"
        backers_elem = BROWSER.find_element(By.XPATH, '//div[@class="mb0"]/h3[@class="mb0"]')
        print "Backers: " + backers_elem.text
        start_period_elem = BROWSER.find_element(By.XPATH, '//p[@class="f5"]/time[1]')
        end_period_elem = BROWSER.find_element(By.XPATH, '//p[@class="f5"]/time[2]')
        print "Funding Period: " + start_period_elem.text + " - " + end_period_elem.text +"\n"

        BROWSER.close()
        BROWSER.switch_to_window(windows_before)
        time.sleep(DELAYS.get("go_back_load", TIME_DEFAULT))
        if PROJECT_COUNT == 12:
            load_more_elem = BROWSER.find_element(By.XPATH, '//a[text()="Load more"]')
            load_more_elem.click()
            time.sleep(DELAYS.get("page_load", TIME_DEFAULT))
    
if __name__ == '__main__':
    LOG.info("Running the Script")
    browser = init_browser()
    LOG.info(browser)
    if not browser:
        LOG.error("Unable to initialize Browser.")
        sys.exit()
    get_kickstarter_page(browser)
    search(browser)
    explore_projects(browser)
    get_project_details(browser)
