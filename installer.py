import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options

from credentials  import username, password


options = Options()
options.set_headless(headless = True)
driver = webdriver.Firefox(firefox_options = options)
print "Running Firefox in headless mode"
driver.get("https://www.instagram.com/particle_io/")
assert "Particle" in driver.title

print "Waiting for the page to load all elements"
time.sleep(5)
print "Done"

login_elem = driver.find_element(By.XPATH, '//button[text()="Log In"]')
login_elem.click()

print "Sleeping to load the Log In Page"
time.sleep(10)
print "Done"

username_elem = driver.find_elements_by_xpath("//input[@name='username']")
ActionChains(driver).move_to_element(username_elem[0]).click().send_keys(username).perform()

password_elem = driver.find_elements_by_xpath("//input[@name='password']")
ActionChains(driver).move_to_element(password_elem[0]).click().send_keys(password).perform()

print "Sleeping to verify Login Info"
time.sleep(3)
print "Done"

login_elem1 = driver.find_element(By.XPATH, '//button[text()="Log in"]')
login_elem1.click()

print "Sleeping to load Home page"
time.sleep(8)
print "Done"

#if (close_elem = driver.find_element(By.XPATH, '//button[text()="Close"]')):
#   close_elem.click()

#search_elem = driver.find_elements_by_xpath("//input[@placeholder='Search']")
#ActionChains(driver).move_to_element(search_elem[0]).click().send_keys("particleio").perform()


driver.get("https://www.instagram.com/particle_io/")
assert "Particle" in driver.title

print "Sleeping to load Particle IO profile page."
time.sleep(5)
print "Done"

followers_elem = driver.find_element_by_partial_link_text("followers")
followers_elem.click()

print "Waiting to load its Followers"
time.sleep(5)
print "Done"


scroll_bar = driver.find_element_by_xpath('//div[@role="dialog"]//a')

min = 2
max = 8
count = 0

def get_one_page_followers():
    
    try:
        print "Try Block"
        follow_button = driver.find_elements(By.XPATH, '//button[(text()="Follow")]')
        for follower in follow_button:
            print follower
            # ActionChains(driver).move_to_element(Follow_elem[0]).click().perform()
            #    if follower == driver.find_element(By.XPATH, '//button[text()="Follow"]'):
            while follower.is_displayed() == False:
                ActionChains(driver).send_keys(Keys.END).perform()

            ActionChains(driver).move_to_element(follower).click(follower).perform()
            print "Waiting for click on follow to complete"
            delay_time = random.randint(min, max)
            time.sleep(delay_time)
            print "Done"
            print "Followed"
            ActionChains(driver).send_keys(Keys.DOWN).perform()
            #
            driver.save_screenshot('/home/ashwin/Downloads/headless_insta.png')
            print "Screenshot Saved to Downloads."
            #
    except:
        print "Except Block"
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(3)

while True:
    get_one_page_followers()
    scroll_bar.send_keys(Keys.END)
    time.sleep(3)

#driver.close()
