# Imports
import sys
import time
import secure
from selenium import webdriver
from selenium.webdriver.common.by import By

# Username and Password from Secure
username = secure.username
password = secure.password

# URLs for Webdriver Configuration
URL_sensical= "https://www.sensical.net/controlpanel/"
URL_timeclock = 'https://www.sensical.net/controlpanel/timeclocklanding.servlet'
URL_kayako = "https://servicedesk.sensical.net/5/staff/"

def DUO_prompt():
    # Function Name: 
    #      DUO_prompt
    # Description: 
    #      Gets a DUO code for MFA during login 
    # Parameters: 
    #      N/A
    # Returns:
    #     string: String of numbers containing a DUO code
    if len(sys.argv) < 2:
        print("")
        print("-" * 10)
        duo_code = input("DUO Code: ")
        print("-" * 10)
    else:
        duo_code = sys.argv[1]
        
    return duo_code

def setup_driver(domain):
    # Function Name: 
    #     setup_driver
    # Description: 
    #     Configures the Chrome Webdriver with necessary Options
    # Parameters:
    #     domain (string): URL for the webdriver to Get
    # Returns:
    #     driver: A configured webdriver to access webpages
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    #options.add_argument("--log-level=3")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(domain)
    return driver

def sensical_login_process(driver, duo_code):
    # Function Name: 
    #     sensical_login_process
    # Description: 
    #     Steps through the Sensical Control Panel login process
    # Parameters:
    #     driver (driver): Chrome Webdriver that drives the automation
    #     duo_code (string): 6 digit code used for MFA
    # Returns:
    #     N/A
    form_username = driver.find_element(by=By.NAME, value="un")
    form_username.clear()
    form_username.send_keys(username)


    form_password = driver.find_element(by=By.NAME, value="pw")
    form_password.clear()
    form_password.send_keys(password)

    submit_button_1 = driver.find_element(by=By.ID, value="field3")
    submit_button_1.click()

    time.sleep(1)
    form_duoprompt = driver.find_element(by=By.NAME, value="pw")
    form_duoprompt.send_keys(duo_code)

    time.sleep(1)
    submit_button_2 = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/form/input[8]')
    driver.implicitly_wait(5)
    submit_button_2.click()

def kayako_login_process(driver):
    # Function Name: 
    #     kayako_login_process
    # Description: 
    #     Steps through the Kayako Servicedesk login process
    # Parameters:
    #     driver (driver): Chrome Webdriver that drives the automation
    # Returns:
    #     N/A
    form_username = driver.find_element(by=By.NAME, value="username")
    form_username.clear()
    form_username.send_keys(username)

    form_password = driver.find_element(by=By.NAME, value="password")
    form_password.clear()
    form_password.send_keys(password)

    form_button = driver.find_element(by=By.NAME, value="submitbutton")
    form_button.click()

def teardown_driver(driver):
    # Function Name: 
    #     teardown_driver
    # Description: 
    #     Destroys the given driver and closes the connection
    # Parameters:
    #     driver (driver): Chrome Webdriver that drives the automation
    # Returns:
    #     N/A
    driver.quit()