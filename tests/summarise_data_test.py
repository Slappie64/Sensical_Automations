# Imports
import login
import time
from datetime import datetime
import csv
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict
from selenium.webdriver.common.by import By   

cleaned_data = pd.read_csv("./data/timesheet_data.csv",
                           usecols=[0,1,2],  
                           encoding='unicode_escape')

agg_sum_time = {'Time Spent' : 'sum'}

df_group = cleaned_data.groupby('Department')

data_dict = {}

for department in df_group.groups.keys():
    int_dict = {}
    grouped_work_date = df_group.get_group(department,).groupby('Work Date').agg(agg_sum_time)
    for row in grouped_work_date.iterrows():
        for data in row[1]:
            int_dict[row[0]] = data
            
    #print("{} - {}".format(department, int_dict))
    data_dict[department] = int_dict

for department, work_date in data_dict.items():
    day_of_week = 0
    print(department)
    for a, b in work_date.items():
        print("{}: {} - {}".format(day_of_week, a, b))
        day_of_week += 1