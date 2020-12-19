from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

def main():
    speed_test_typer()

def speed_test_typer():
    path = 'C:\Program Files (x86)\chromedriver.exe'
    global driver
    driver = webdriver.Chrome(path)

    driver.get('https://10fastfingers.com/typing-test/english')
    time.sleep(2)

    # click "allow selection"
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelection"]')))
    element.click()

    # click login
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="speedtest-main"]/div[5]/div[1]/div[1]/a')))
    element.click()

    # click google
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="login-btns"]/ul/li[3]/a')))
    element.click()

    # click input email
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
    element.send_keys('jasonsminhas@gmail.com')
    element.send_keys(Keys.RETURN)

    # click input password
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
    element.send_keys('Islandbox1')
    element.send_keys(Keys.RETURN)

    # find text
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'row1'))
    )

    source = element.get_attribute('outerHTML')
    type_text = BeautifulSoup(source, 'lxml')
    type_list = [line.next for line in type_text.find_all('span')]

    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'inputfield'))
    )

    time.sleep(2)

    for word in type_list:
        element.send_keys(word)
        element.send_keys(' ')

    print('stop')


if __name__ == '__main__':
    main()