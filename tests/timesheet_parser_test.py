# Imports
import login
import time
from datetime import datetime
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

DUO_code = login.DUO_prompt()
driver = login.setup_driver(login.URL_sensical)

login.sensical_login_process(driver, DUO_code)

timeclock_link = driver.find_element(by=By.LINK_TEXT, value="Timesheets")
timeclock_link.click()

time.sleep(2)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

table = soup.find(attrs={'class': 'tdproj gsc'})
rows = table.findChildren('tr', attrs={'class': 'trEntry'})

row_title = soup.findChildren('input')



for child in row_title:
    print(child)