from selenium import webdriver
import time
from os import environ
import sys


def login_to_codechef(driver):
    wait_time = 7
    driver.get('https://www.codechef.com/')
    time.sleep(wait_time)
    driver.find_element_by_id('edit-name').send_keys(environ.get('CODECHEF_USER'))
    driver.find_element_by_id('edit-pass').send_keys(environ.get('CODECHEF_PASS'))
    driver.find_element_by_id('edit-submit').click()
    while 'limit' in driver.current_url:
        driver.find_element_by_class_name('form-checkbox').click()
        driver.find_element_by_class_name('form-submit').click()
        time.sleep(wait_time)



def submit_solution(driver, problem_code, full_solution_path):
    wait_time = 7
    driver.get('https://www.codechef.com/submit/' + problem_code)
    time.sleep(wait_time)
    file_path = full_solution_path
    driver.find_element_by_class_name('form-file').send_keys(file_path)
    driver.find_element_by_xpath('/html/body/center/center/table/tbody/tr/td/div/div/div/div[2]/form[2]/div/div[2]/div[3]/select/option[2]').click()
    driver.find_element_by_xpath('/html/body/center/center/table/tbody/tr/td/div/div/div/div[2]/form[2]/div/div[2]/input[5]').click()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Retry : python3 xxx.py xxx.cpp /abc/def/.../xxx.cpp")
    driver = webdriver.Chrome('/Users/ayushanshul07/ayush/selenium_practice/chromedriver')
    login_to_codechef(driver)
    submit_solution(driver,sys.argv[1],sys.argv[2])

