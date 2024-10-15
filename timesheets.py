# Imports
import login
import time
from datetime import datetime
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def run_kayako_report():
    # Function Name: 
    #     run_kayako_report
    # Description: 
    #     Runs a Kayako report on ticket time then exports as CSV
    # Parameters:
    #     driver (driver): Chrome Webdriver that drives the automation
    # Returns:
    #     N/A
    driver = login.setup_driver(login.URL_kayako)

    login.kayako_login_process(driver)

    time.sleep(2)
    reports_toplevel = driver.find_element(by=By.ID, value="tb_menusection9")
    reports_toplevel.click()

    reports_manage = driver.find_element(by=By.ID, value="linkmenu9_0")
    reports_manage.click()

    time.sleep(1)
    tickets_timeworked_weekly = driver.find_element(by=By.LINK_TEXT, value="Tickets_TimeWorked_Weekly")
    tickets_timeworked_weekly.click()

    time.sleep(1)
    run_report = driver.find_element(by=By.ID, value="View_Report2form_submitform_0")
    run_report.click()

    kayako_report_data_export(driver)

def kayako_report_data_export(driver):
    # Function Name: 
    #     kayako_report_data_export
    # Description: 
    #     Scrape data from the report using BeautifulSoup
    # Parameters:
    #     driver (driver): Chrome Webdriver that drives the automation
    # Returns:
    #     Scraped and organised data from Timesheet Report
    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(attrs={'class': 'reportstable'})
    row = table.find_all('tr')

    with open('./data/timesheet_data_raw.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        ticket_headers = []

        for ticket in row[0]:
            for info in ticket:
                if not info.isspace():
                    ticket_headers.append(info)
        writer.writerow(ticket_headers)
    
        for ticket in row[1:]:
            ticket_info = []
            for info in ticket:
                if not info.text.isspace():
                    ticket_info.append(info.text)
            writer.writerow(ticket_info)

    login.teardown_driver(driver)

def display_data(data):
    
    # Function Name: 
    #     display_data
    # Description: 
    #     Takes a grouped dictionary and prints it to the console.
    # Parameters:
    #     <data> (dict): Grouped dictionary containing departmets and time worked.
    # Returns:
    #     N/A
    print("Timesheets")
    for department, day in data.items():
        iterator = 0
        print(department)
        for date, time in day.items():
            print("{}: {} - {}".format(iterator, date, time))
            iterator += 1

def clean_summ_data():
    # Function Name: 
    #     clean_summ_data
    # Description: 
    #     Remove unused columns 0 and 3 from the raw data.
    #     Summarise the collected data into total hours / minutes per day
    # Parameters:
    #     N/A
    # Returns:
    #     data_dict: Dictionary ordered by Department and Date with sum time spent
    file = pd.read_csv("./data/timesheet_data_raw.csv", usecols=[1,2,4,5,6,7,8], encoding='unicode_escape')
    for index, row in file.iterrows():
        #print(row['Work Date'], row['Time Spent'])
        converted_date = datetime.strptime(row['Work Date'], '%d %b %Y %H:%M').date()
        try:
            converted_time_worked = datetime.strptime(row['Time Spent'], '%Hh %Mm %Ss' )
        except ValueError:
            converted_time_worked = datetime.strptime(row['Time Spent'], '%Mm %Ss' )

        file.at[index, 'Work Date'] = converted_date.strftime("%d/%m")
        file.at[index, 'Time Spent'] = converted_time_worked.strftime("%M")

    file.to_csv("./data/timesheet_data.csv", index=False)
    
    cleaned_data = pd.read_csv("./data/timesheet_data.csv",
                           usecols=[0,1,2],  
                           encoding='unicode_escape')

    df_group = cleaned_data.groupby('Department')
    agg_sum_time = {'Time Spent' : 'sum'}

    data_dict = {}

    for department in df_group.groups.keys():
        int_dict = {}
        grouped_work_date = df_group.get_group(department,).groupby('Work Date').agg(agg_sum_time)
        for row in grouped_work_date.iterrows():
            for data in row[1]:
                int_dict[row[0]] = data       
        data_dict[department] = int_dict

    for department, work_date in data_dict.items():
        day_of_week = 0
        for a, b in work_date.items():
            day_of_week += 1

    return(data_dict)

#TODO - Import summarised data into Timesheet
def import_data(data):
    # Function Name: 
    #     import_data
    # Description: 
    #     Imports the data into my timesheet
    # Parameters:
    #     data (dataframe): Cleaned and summarised data created from summarise_data()
    # Returns:
    #     <bool>: True or False whether this upload was successful or not
    DUO_code = login.DUO_prompt()
    driver = login.setup_driver(login.URL_sensical)

    login.sensical_login_process(driver, DUO_code)

    timeclock_link = driver.find_element(by=By.LINK_TEXT, value="Timesheets")
    timeclock_link.click()

    time.sleep(2)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(attrs={'class': 'tbodyEntries'})
    row = table.find_all(attrs={'class' : 'trEntry'})

    for i in row:
        print(i)

def log_complete_data(data):
    with open('./data/test.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        timesheet_header = ["Department"]

        for key, values in data:
            for i in values.keys():
                timesheet_header.append(i)
        writer.writerow(timesheet_header)
        
        

"""
if __name__ == '__main__':
    try:
        
    except:
        print("Something went wrong, please try again")
"""

run_kayako_report()
display_data(clean_summ_data())
#import_data()