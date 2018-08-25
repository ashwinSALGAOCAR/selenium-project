from datetime import datetime as dt
import logging
import random
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from credentials  import username, password

BROWSER = None

FOLLOW_CLICK_SUCCESS = ['Following', 'Requested']
FOLLOW_CLICK_FAILURE = ['Follow']

LOG = logging.getLogger('follow_service')
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


DELAYS = {"scroll_wait": 1, 'page_load': 3, 'follow_attemp_status': 5, 'load_followers': 5}

ELAPSED_TIME_LIMIT = 45

MAX_FOLLOWED = 39

START_TIME = dt.now()


def sleep(wait_type):
    default_wait = 5
    time.sleep(DELAYS.get(wait_type, default_wait))

def get_time_elapsed():
    curr_time = dt.now()
    diff = curr_time - START_TIME
    return diff.seconds / 60

def check_time_elapsed(browser):
    if get_time_elapsed() > ELAPSED_TIME_LIMIT:
        LOG.error("Script is running to slow so quitting")
        stop_script(browser)



def init_browser(headless=False):
    options = Options()
    options.set_headless(headless = headless)
    BROWSER = webdriver.Firefox(firefox_options = options)
    BROWSER.set_window_size(800, 750)
    #BROWSER = webBROWSER.Firefox()
    LOG.info("Running Firefox in headless mode")
    return BROWSER
    

def insta_login(BROWSER):
    BROWSER.get("https://www.instagram.com/particle_io/")
    assert "Particle" in BROWSER.title


    LOG.info("Waiting for the page to load all elements")
    time.sleep(DELAYS.get("page_load", 5))
    LOG.info("Done")

    login_elem = BROWSER.find_element(By.XPATH, '//button[text()="Log In"]')
    login_elem.click()

    LOG.info("Sleeping to load the Log In Page")
    sleep("page_load")
    LOG.info("Done")

    username_elem = BROWSER.find_elements_by_xpath("//input[@name='username']")
    ActionChains(BROWSER).move_to_element(username_elem[0]).click().send_keys(username).perform()

    password_elem = BROWSER.find_elements_by_xpath("//input[@name='password']")
    ActionChains(BROWSER).move_to_element(password_elem[0]).click().send_keys(password).perform()

    LOG.info("Sleeping to verify Login Info")
    time.sleep(3)
    LOG.info("Done")

    login_elem1 = BROWSER.find_element(By.XPATH, '//button[text()="Log in"]')
    login_elem1.click()

    LOG.info("Sleeping to load Home page")
    sleep("page_load")
    LOG.info("Done")

#if (close_elem = BROWSER.find_element(By.XPATH, '//button[text()="Close"]')):
#   close_elem.click()

#search_elem = BROWSER.find_elements_by_xpath("//input[@placeholder='Search']")
#ActionChains(BROWSER).move_to_element(search_elem[0]).click().send_keys("particleio").perform()

def go_to_user_followers(BROWSER,user):
    BROWSER.get("https://www.instagram.com/particle_io/")
    assert "Particle" in BROWSER.title

    LOG.info("Sleeping to load Particle IO profile page.")
    time.sleep(DELAYS.get("page_load", 5))
    LOG.info("Done")

def open_followers_list(BROWSER):
    followers_elem = BROWSER.find_element_by_partial_link_text("followers")
    LOG.info("This is the followers element %s", followers_elem)
    # print ("dir follower ", dir(followers_elem))
    # BROWSER.execute_script("return arguments[0].scrollIntoView();", followers_elem)
    # followers_elem.click()
    ActionChains(BROWSER).move_to_element(followers_elem).click(followers_elem).perform()
    LOG.info("Waiting to load its Followers")
    sleep("load_followers")
    LOG.info("Done")

def get_scroll_bar(BROWSER):
    try:
        scroll_bar = BROWSER.find_element_by_xpath('//div[@role="dialog"]//a')
        return scroll_bar
    except NoSuchElementException as e:
        LOG.exception(e)
        LOG.error("Could not open the followers popup hence Quitting")
        BROWSER.close()
        sys.exit()
        scroll_bar = BROWSER.find_element_by_xpath('//div[@role="dialog"]//a')
        return scroll_bar

def stop_script(BROWSER):
    global total_count
    BROWSER.close()
    LOG.info("This is the FOLLOWED TOTAL COUNT before quitting %s", total_count)
    sys.exit()



def follow_user(BROWSER, follower):
    global total_count
    global unsuccessful_count
    try:
        ActionChains(BROWSER).move_to_element(follower).click(follower).perform()
        LOG.info ("Waiting for click on follow to complete")
        LOG.info("This is the element text before clicking: %s:", follower.text)        
        delay_time = random.randint(min, max)
        LOG.info("Clicked on Follow")


        # ActionChains(BROWSER).send_keys(Keys.DOWN).perform()
        # Checking for limit of 42 followers
        if total_count > MAX_FOLLOWED:
            LOG.info("Crossed the Max followed limit of %s users. Quitting script", MAX_FOLLOWED)
            stop_script(BROWSER)

        time.sleep(delay_time)
        status = follower.get_attribute("attribute name")
        LOG.info("This is the element text after clicking: %s:", follower.text)
        if follower.text in FOLLOW_CLICK_SUCCESS:
            total_count+= 1
            LOG.info("Followed successfully")
            LOG.info("Follwed count : "+ str(total_count))
        elif follower.text in FOLLOW_CLICK_FAILURE:
            LOG.error("Could not follow")
            unsuccessful_count +=1
            LOG.error("Failed follow counts: %s", unsuccessful_count)
            if unsuccessful_count > 10:
                LOG.error("Cannot follow users due to rate limit hence quitting")
                LOG.info("TOTAL COUNT: %s", total_count)
                stop_script(BROWSER)


        # BROWSER.save_screenshot('/home/vagrant/repos/selenium-project-master/headless_insta.png')
        # LOG.info("Screenshot Saved to Downloads.")
        return True

    except MoveTargetOutOfBoundsException as e:
        LOG.error("Outside the viewport range")
        LOG.exception(e)
        LOG.info("scrolling to the element")
        BROWSER.execute_script("return arguments[0].scrollIntoView();", follower)
        return False
    except StaleElementReferenceException as e:
        LOG.error("The element is become stale so ignoring it")
        LOG.exception(e)
        return True

    except Exception as e:
        LOG.error("Inside except block of follow_user")
        LOG.exception(e)
        return False



min = 3
max = 8
total_count = 0
unsuccessful_count = 0

def get_one_page_followers(BROWSER,scroll_bar):
    count = 0
    LOG.debug('Inside get followers')
    try:
        LOG.debug("Try Block")
        followers = BROWSER.find_elements(By.XPATH, '//button[(text()="Follow")]')

        for i, follower in enumerate(followers):
            LOG.info("%s --> %s", i, follower)
            check_time_elapsed(BROWSER)
            # ActionChains(BROWSER).move_to_element(Follow_elem[0]).click().perform()
            #    if follower == BROWSER.find_element(By.XPATH, '//button[text()="Follow"]'):
            while True:
                status = follower.is_displayed()
                if status:
                    break
                LOG.info('Follower not displayed. Going to the end')
                scroll_bar.send_keys(Keys.END)
                # ActionChains(BROWSER).send_keys(Keys.END).perform()

            retry_following_count = 0
            while True:
                status = follow_user(BROWSER, follower)
                if status:
                    break

                if retry_following_count > 5:
                    LOG.error("Tried following the user multiple times but could not find. So exiting script")
                    BROWSER.close()
                    sys.exit()
                retry_following_count += 1
                LOG.error("Unable to follow user so scrolling down")
                # scroll_bar.send_keys(Keys.DOWN)

        LOG.info('Done with get_one_page_followers ') 
            # #
            # while follower.is_displayed() == False:
            #     LOG.info('Follower not displayed. Going to the end')
            #     ActionChains(BROWSER).send_keys(Keys.DOWN).perform()

    except Exception as e:
        LOG.error("Except Block of get followers")
        LOG.error(e)
        scroll_bar.send_keys(Keys.DOWN)
        # ActionChains(BROWSER).send_keys(Keys.PAGE_DOWN).perform()
        LOG.error("Waiting for 20 seconds")
        time.sleep(5)

#BROWSER.close()


if __name__ == '__main__':
    try:
        LOG.info('Running as script')
        browser = init_browser()
        LOG.info(BROWSER)
        if not browser:
            LOG.error('Unable to initialize browser')
            sys.exit()

        insta_login(browser)
        go_to_user_followers(browser,'test')
        open_followers_list(browser)
        scroll_bar = get_scroll_bar(browser)
        LOG.debug(scroll_bar)
    except Exception as e:
        LOG.error("Exception before following")
        if browser:
            browser.close()
        sys.exit()


    while True:
        try:
            get_one_page_followers(browser,scroll_bar)
            scroll_bar.send_keys(Keys.END)
            LOG.debug("Waiting inside while True")
            check_time_elapsed(browser)
            sleep('scroll_wait')
            # sys.exit()
        except Exception as e:
            LOG.error('Inside Except block of while true')
            LOG.error(e)
            open_followers_list(browser)
            scroll_bar = get_scroll_bar(browser)
            LOG.info("Got the scroll_bar %s", scroll_bar)
