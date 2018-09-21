import sys
import time
import random
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options


BROWSER = None
TIME_DEFAULT = 5
PROJECT_COUNT = 0
PAGE_COUNT = 1
DELAYS = {'page_load': 3, 'search_load': 4, 'ajax_load': 2, 'go_back_load': 1}

SUCCESSFUL_PROJECTS_LIST = open("Successful_project_list.txt", "w+")
LOG = logging.getLogger('Kickstarter_Search_Service')
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level = logging.INFO, format = FORMAT)


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

def total_projects(BROWSER):
    total_proj_elem = BROWSER.find_element(By.XPATH, '//b[@class="count ksr-green-500"]')
    total_projects = total_proj_elem.text
    int_total = total_projects.split(' ')
    SUCCESSFUL_PROJECTS_LIST.write("Listing " + int_total[0] + " " + int_total[1] + "\n\n")
    print "\nListing " + int_total[0] + " " + int_total[1]
    time.sleep(DELAYS.get("projects_load", TIME_DEFAULT))
    return int(int_total[0])

def open_new_tab(BROWSER, project_link):
    windows_before  = BROWSER.current_window_handle
    BROWSER.execute_script('''window.open('', "project_link_blank");''')
    LOG.info("Opening New Tab")
    windows_after = BROWSER.window_handles
    new_window = [x for x in windows_after if x != windows_before][0]
    BROWSER.switch_to_window(new_window)
    BROWSER.get(project_link)
    time.sleep(DELAYS.get("page_load", TIME_DEFAULT))
    return windows_before

def get_project_data(BROWSER):
    title = (BROWSER.find_element(By.XPATH, '//a[@class="hero__link"]')).text
    fund = (BROWSER.find_element(By.XPATH, '//h3/span[@class="money"]')).text
    pledge = (BROWSER.find_element(By.XPATH, '//div[@class="type-12 medium navy-500"]/span[@class="money"]')).text
    backers = (BROWSER.find_element(By.XPATH, '//div[@class="mb0"]/h3[@class="mb0"]')).text
    start_period = (BROWSER.find_element(By.XPATH, '//p[@class="f5"]/time[1]')).text
    end_period = (BROWSER.find_element(By.XPATH, '//p[@class="f5"]/time[2]')).text
    return title, fund, pledge, backers, start_period, end_period

def get_project_duration(start_period, end_period):
    launch_date = datetime.strptime(start_period, '%b %d %Y')
    success_date = datetime.strptime(end_period, '%b %d %Y')
    duration = str(success_date - launch_date).split(' ')
    return duration[0]+" "+duration[1].replace(',','')

def print_to_console(project_link, title, funds, pledged, backers, start_period, end_period):
    print "Project " + str(PROJECT_COUNT) + ":" + project_link
    print "Title: " + title
    print "Total Funding: " + funds
    print "Plegded amount: " + pledged
    print "Backers: " + backers
    print "Funding Period: " + start_period + " - " + end_period +" (" + get_project_duration(start_period, end_period)  + ")\n"

def save_to_file(project_link, title, funds, pledged, backers, start_period, end_period):
    SUCCESSFUL_PROJECTS_LIST.write("Project " + str(PROJECT_COUNT) + ":" + project_link + "\n")
    SUCCESSFUL_PROJECTS_LIST.write("Title: " + title.encode('utf-8') + "\n")
    SUCCESSFUL_PROJECTS_LIST.write("Total Funding: " + funds.encode('utf-8') + "\n")
    SUCCESSFUL_PROJECTS_LIST.write("Plegded amount: " + pledged.encode('utf-8') + "\n")
    SUCCESSFUL_PROJECTS_LIST.write("Backers: " + backers.encode('utf-8') + "\n")
    SUCCESSFUL_PROJECTS_LIST.write("Funding Period: " + start_period.encode('utf-8') + " - " + end_period.encode('utf-8') + " (" + get_project_duration(start_period, end_period)  + ")\n\n")
    
def close_current_tab(BROWSER, windows_before):
    BROWSER.close()
    BROWSER.switch_to_window(windows_before)
    time.sleep(DELAYS.get("go_back_load", TIME_DEFAULT))
    
def get_project_details(BROWSER):
    global PROJECT_COUNT
    global PAGE_COUNT
    proj_list_elem = BROWSER.find_elements(By.XPATH, '//div[@id="projects_list"]/div[' + str(PAGE_COUNT) + ']/div/div/div/div/div[2]/a[@class="block img-placeholder w100p"]')
    for project in proj_list_elem:
        project_link =  project.get_attribute('href')
        PROJECT_COUNT += 1
        
        windows_before = open_new_tab(BROWSER, project_link)
        title, funds, pledged, backers, start_period, end_period = get_project_data(BROWSER)
        print_to_console(project_link, title, funds, pledged, backers, start_period, end_period)
        save_to_file(project_link, title, funds, pledged, backers, start_period, end_period)
        close_current_tab(BROWSER, windows_before)

        if PROJECT_COUNT % 12 == 0:
            PAGE_COUNT += 1
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
    all_projects = total_projects(browser)
    while True:
        get_project_details(browser)
        if PROJECT_COUNT == all_projects:
            browser.close()
            LOG.info("Done with all projects!")
            sys.exit()
