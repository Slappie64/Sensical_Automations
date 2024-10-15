# Imports
import login
from selenium.webdriver.common.by import By


def clock_in():
    # Function Name: 
    #     clock_in
    # Description: 
    #     Navigates the Sensical Control Panel and clocks in
    # Parameters:
    #     N/A
    # Returns:
    #     N/A
    DUO_code = login.DUO_prompt()
    driver = login.setup_driver(login.URL_sensical)

    login.sensical_login_process(driver, DUO_code)

    timeclock_link = driver.find_element(by=By.LINK_TEXT, value="Timeclock")
    timeclock_link.click()

    timeclock_button = driver.find_element(by=By.XPATH, value='//*[@id="form_timeclock"]/table[1]/tbody/tr/td[2]/input')
    timeclock_button.click()

    timeclock_status = driver.find_element(by=By.CLASS_NAME, value="rag")

    print("")
    print("-" * len(timeclock_status.text))
    print(timeclock_status.text)
    print("-" * len(timeclock_status.text))

    login.teardown_driver(driver)

if __name__ == '__main__':
    try:
        clock_in()
    except:
        print("Something went wrong, please try again")