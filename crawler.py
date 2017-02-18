from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# geckdriver setup
# Download the geckodriver from here
# Extract and unzip and move the geckodriver file to /usr/local/bin/ directory

driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
# driver = webdriver.Firefox()
# driver.implicitly_wait(10)
driver.get('https://www.twitch.tv/dreamhackcs')
#
print("Current url: ", driver.current_url)
player = driver.find_element_by_id('player')
player.click()
ActionChains(driver).key_down(Keys.CONTROL).send_keys('x').key_up(Keys.CONTROL).perform()
# clip_btn = None
# for b in btns:
#     if b.get_attribute('data-tip') == 'Clip (Alt+X)':
#         clip_btn = b
#         break

# clip_btn.click()

print("Now url is: ", driver.current_url)
#
# edit_css = "button.align-center.full-width.ce-button-fancy"
# driver.find_elements_by_css_selector(clip_css)[0].click()
#
# print("Finnaly url is: ", driver.current_url)
# # elem.send_keys("pycon")
# # elem.send_keys(Keys.RETURN)
# # assert "No results found." not in driver.page_source
# # print(driver.title)
driver.close()
