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
from filereader import read, write
from automation import Automation
from parsers import parse_name, parse_records
# private helper 
def followAppointment(automation, date, reason):
    #click autocomplete follow up
    automation.click('//input[@id="visit-type-lookupIpt1"]')

    # select follow up
    automation.click('//a[@id="visit-type-lookupLink1ngR12"]')
    #set date
    
    print('attempting to set date')
    datebox = automation.find('//input[@id="Appt_startDate"]')
    print('found date box')
    datebox.click()
    datebox.clear()
    datebox.send_keys(date + Keys.ENTER)
    print('set date')
    timestart = automation.find('//input[@placeholder="Start Time"]')
    print('found time start')
    timeend = automation.find('//input[@placeholder="End Time"]')
    print('reason')
    reason_box = automation.find('//input[@placeholder="Enter reason"]')
    reason_box.send_keys(reason)
    print('found time end')
    timestart.click()
    timestart.clear()
    
    timestart.send_keys(automation.get_time())
    automation.hour+=1
    timeend.click()
    timeend.clear()
    timeend.send_keys(automation.get_time())
    print('set time and date')

    time.sleep(1)

# main function to create appointment
def createAppointment(automation, name, date, reason):
    automation.click('//a[@id="jellybean-panelLink65"]')
    #variable
    time.sleep(1)
    searchbox = automation.find('//input[@id="searchText"]')
    searchbox.send_keys(name)
    time.sleep(1)
    automation.tryClick('//button[@data-dismiss="modal"]',2)
    automation.click('//span[@id="patientLName1"]')
    print('searched ' + name)

    # click new appointment button
    automation.click('//button[@id="patient-hubBtn6"]')
    print('clicked new appointment')

    # try cancel popup
    time.sleep(2)
    automation.tryClick('//button[@id="billingAlertBtn6"]')

    followAppointment(automation, date, reason)

    # click ok
    automation.click('//button[@id="newAppointmentBtn51"]')
    print('clicked ok to create appointment')

    # try dismiss second popup
    time.sleep(2)
    automation.tryClick('//button[@data-bb-handler="confirm"]')
    

    # close patient modal
    automation.click('//button[@id="patient-hubBtn1"]')
    print('closed appointment modal')
    time.sleep(2)

def create_all_appointments(automation):
    store = read()
    for row in store:
        try:
            appt_type = row['appointment_type'].lower()
            name = parse_name(row['name'])
            date = datetime.strptime(row['appt_date'], "%m/%d/%Y").strftime("%m/%d/%Y")
            reason = row['reason']
            status = row['appt_status']
            if appt_type != 'f' or status in ('created', 'error'):
                print('skipping appointment for', name)
                continue

            createAppointment(automation, name, date, reason)
            row['appt_status'] = 'created'
        except Exception as e:
            print('something went wrong creating appointment for', name, e)
            automation.driver.refresh()
            time.sleep(5)
        finally:
            # try close patient modal
            automation.tryClick('//button[@id="patient-hubBtn1"]',1)
    
    print('Done creating all appointments')
    write(store)

