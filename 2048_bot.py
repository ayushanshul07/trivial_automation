#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


driver = webdriver.Chrome('/Users/ayushanshul07/ayush/selenium_practice/chromedriver')
driver.get('https://play2048.co')

count = 0
while True:
    count = (count + 1)%4
    if count == 0:
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_DOWN)
    if count == 1:
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_LEFT)
    if count == 2:
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
    if count == 3:
        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_RIGHT)
    try:
        WebDriverWait(driver, 0.5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div[1]')))
        break
    except TimeoutException as Ex:
        continue
print('Your final score is: ' + driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div[1]').text)
driver.quit()
