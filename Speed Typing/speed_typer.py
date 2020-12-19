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

    # find text
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'row1'))
    )

    #  get list of word to type
    source = element.get_attribute('outerHTML')
    type_text = BeautifulSoup(source, 'lxml')
    type_list = [line.next for line in type_text.find_all('span')]

    # find input box for words
    element = WebDriverWait(driver, 8).until(
        EC.presence_of_element_located((By.ID, 'inputfield'))
    )

    time.sleep(2)

    # input words 
    for word in type_list:
        element.send_keys(word)
        element.send_keys(' ')


if __name__ == '__main__':
    main()