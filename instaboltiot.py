import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from credentials  import username, password

driver = webdriver.Firefox()
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

#Follow new users
followers = driver.find_elements(By.XPATH, '//button[text()="Follow"]')
'''+ driver.find_elements(By.XPATH, '//button[text()="Following"]') + driver.find_elements(By.XPATH, '//button[text()="Requested"]')'''

print "Sleeping to load scroll bar element"
time.sleep(4)
print "Done"

scroll_bar = driver.find_element_by_xpath('//div[@role="dialog"]//a')

min = 2
max = 8
count = 0

actions = ActionChains(driver)

for follower in followers:
    print follower
    # ActionChains(driver).move_to_element(Follow_elem[0]).click().perform()
#    if follower == driver.find_element(By.XPATH, '//button[text()="Follow"]'):
    actions.move_to_element(follower)
    actions.click(follower).perform()
#    follower.click()
    print "Waiting to click follow to complete"
    time.sleep(3)
    print "Done"
    scroll_bar.send_keys(Keys.DOWN)
    print "Followed"
    delay_time = random.randint(min, max)
    time.sleep(delay_time)
'''    elif follower == driver.find_element(By.XPATH, '//button[text()="Requested"]'):
        print follower
        print "Requested"
        delay_time = random.randint(min, max)
        time.sleep(delay_time)
    elif follower == driver.find_element(By.XPATH, '//button[text()="Following"]'):
        print follower
        print "Following"
        delay_time = random.randint(min, max)
        time.sleep(delay_time)
'''

#    count+=1
#    if count ==10:


print "Waiting to get to the end of follwers page"
time.sleep(5)
print "Done"

#element_inside_popup = driver.find_element_by_xpath('//div[@role="dialog"]//a')
scroll_bar.send_keys(Keys.END)

#username_elem = driver.find_element(By.XPATH, '//label[text()="Phone number, username, or email"]')


#login_elem = driver.find_element_by_class("")
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem_go = driver.find_element_by_id("submit")
#elem_go.click()
#assert "No results found." not in driver.page_source
#driver.close()


