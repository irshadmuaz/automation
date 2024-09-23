from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.chrome.options import Options
import datetime
import time
import threading
from datetime import datetime, timedelta
import json
from filereader import read,write

def extract_vitals(automation, iframeName):
    #automation.driver.get('file:///C:/Users/irsha/Documents/Github/selenium/dash.html')
    automation.switch_to_frame('//iframe[@name="{0}"]'.format(iframeName))
    print('switched to frame')
    cols = automation.find_all('//td[@class="detailColHeader"]')
    columns = [c.text for c in cols]
    rows = [columns]
    tablerows = automation.find_all('//tr[@class="normalRow"]')
    for row in tablerows:
        rows.append([c.text for c in row.find_elements(By.TAG_NAME, 'td')])
    
    automation.driver.switch_to.default_content()
    return rows

def copy_vitals(automation, name, id):
    # Go to point click 
    #automation.driver.get('https://pointclickcare.com/')
    # Click login
    #automation.click('//span[@class="menu-text"]')

    # variable
    element = automation.find('//input[@id="searchField"]')
    print('found search field')
    element.send_keys(name + Keys.ENTER)
    time.sleep(1)
    query = "//a[contains(text(), '{0}')]".format(id)
    automation.tryClick(query, 1)

    time.sleep(1)
    print('starting extraction')
    
    vitals = extract_vitals(automation, 'MostRecentVitals')
    medication = extract_vitals(automation,'Medications')

    return [vitals, medication]

def copy_all_vitals(automation):
    store = read()
    print('here')
    for row in store:
        try:
            [first,last] = row['name'].split(',')
            appt_type = row['appointment_type'].lower()
            # Do not retry if it already has vitals and medications
            if appt_type != 'f' or (row['vitals'] and row['medication']):
                print('skipping', first,last)
                continue
            print('working on ', first)
            [vitals, medication] = copy_vitals(automation, first.strip(), row['name'])
            row['vitals'] = vitals
            row['medication'] = medication
        except Exception as e:
            print('something went wrong copying vitals', e)
            automation.driver.refresh()
            time.sleep(5)
    print('Finished copying all vitals from pointclick')
    write(store)