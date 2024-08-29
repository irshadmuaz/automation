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

#  & 'C:\Program Files\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"
class Automation:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
        self.service = Service('chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.hour = 1
    
    def click(self,xpath, wait=1000):
        elements = WebDriverWait(self.driver, wait).until(lambda x:x.find_elements(By.XPATH, xpath))
        for element in elements:
            try:
                element.click()
            except:
                continue
    
    def get_time(self):
        # Set the start and end times
        start_time = datetime.strptime("8:00 AM", "%I:%M %p")
        end_time = datetime.strptime("10:00 PM", "%I:%M %p")
        current_time =  start_time + timedelta(minutes=15*self.hour)
 
        if current_time > end_time:
            self.hour = 1
        return current_time.strftime("%I:%M %p")
    
    def handle_popup_thread(self):
        while True:
            # try dismiss popup
            self.tryClick('//button[@data-bb-handler="confirm"]',1)
            self.tryClick('//button[@data-bb-handler="No"]',1)
            print('second thread working')
            time.sleep(1)
            
    
    def find(self, xpath, wait=100):
        return WebDriverWait(self.driver, wait).until(lambda x:x.find_element(By.XPATH, xpath))
    
    def find_all(self, xpath, wait=100):
        return WebDriverWait(self.driver, wait).until(lambda x:x.find_elements(By.XPATH, xpath))
    
    def sendkeys(self, element, keys):
        element.send_keys(keys + Keys.ENTER)
    
    def execute(self):
        # Go to point click 
        self.driver.get('https://pointclickcare.com/')
        # Click login
        self.click('//span[@class="menu-text"]')

        # variable
        name = "jones"
        element = self.find('//input[@id="searchField"]')
        time.sleep(2)
        element.send_keys(name + Keys.ENTER)

        #todo copy medications and vitals
    def tryClose(self):
        try:
            self.click('//button[@data-dismiss="modal"]',1)
        except:
            return
        
    def tryClick(self, xpath, wait=10):
        try:
            self.click(xpath, wait)
            print('successfully closed popup ' + xpath, str(datetime.datetime.now()))
        except: 
            return
        
    def eclinic(self):
        pass
        #self.driver.get('https://caazadhaw3mrvlx9ayapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp#/mobiledoc/jsp/webemr/jellybean/officevisit/officeVisits.jsp')
        
    
    def followAppointment(self, date):
        #click autocomplete follow up
        self.click('//input[@id="visit-type-lookupIpt1"]')

        # select follow up
        self.click('//a[@id="visit-type-lookupLink1ngR12"]')
        #set date
      
        print('attempting to set date')
        datebox = self.find('//input[@id="Appt_startDate"]')
        print('found date box')
        datebox.click()
        datebox.clear()
        datebox.send_keys(date + Keys.ENTER)
        print('set date')
        timestart = self.find('//input[@placeholder="Start Time"]')
        print('found time start')
        timeend = self.find('//input[@placeholder="End Time"]')
        print('found time end')
        timestart.click()
        timestart.clear()
        
        timestart.send_keys(self.get_time())
        self.hour+=1
        timeend.click()
        timeend.clear()
        timeend.send_keys(self.get_time())
        print('set time and date')

        time.sleep(1)

    def createAppointment(self, name, date):
        self.click('//a[@id="jellybean-panelLink65"]')
        #variable
        time.sleep(1)
        searchbox = self.find('//input[@id="searchText"]')
        searchbox.send_keys(name)
        time.sleep(1)
        self.tryClose()
        self.click('//span[@id="patientLName1"]')
        print('searched ' + name)

        # click new appointment button
        self.click('//button[@id="patient-hubBtn6"]')
        print('clicked new appointment')

        # try cancel popup
        time.sleep(2)
        self.tryClick('//button[@id="billingAlertBtn6"]')

        self.followAppointment(date)

        # click ok
        self.click('//button[@id="newAppointmentBtn51"]')
        print('clicked ok to create appointment')

        # try dismiss second popup
        time.sleep(2)
        self.tryClick('//button[@data-bb-handler="confirm"]')
        

        # close patient modal
        self.click('//button[@id="patient-hubBtn1"]')
        print('closed appointment modal')
        time.sleep(2)
    
    def parse_meds(self, med):
        lst = eval(med)
        format = []
        for r in lst:
            format.append(' '.join(r[:len(r)-3]))
        return '\n'.join(format)

    def parse_vitals(self, vit):
        lst = eval(vit)
        format = []
        for r in lst:
            format.append(' '.join(r[:len(r)-2]))
        return '\n'.join(format)

    def populate_records(self, store):
        
        elements = self.driver.find_elements(By.XPATH, "//span[starts-with(@id, 'officeVisitsLink')]")
        dictionary = {}
        for element in elements:
            dictionary[element.text]=element
        print(dictionary.keys())
        for row in store:
            name = row['name']
            parts = name.split(' ')
            parts.pop()
            name = ' '.join(parts)
            appt_type = row['appointment_type']
            for key in dictionary.keys():
                try:
                    if key.lower().startswith(name.lower()) and appt_type.lower() == 'f':
                        print('found name', key)
                        dictionary[key].click()
                        self.click('//b[@onclick="pnSectionClicked(\'Medical History:\', event)"]')
                        textbox = self.find('//input[@placeholder="Write text and Press Enter"]')
                        medications = self.parse_meds(row['medication'])
                        vitals = self.parse_vitals(row['vitals'])

                        textbox.send_keys(medications + Keys.ENTER)
                        textbox.send_keys(vitals + Keys.ENTER)
                        # close modal
                        self.click('//button[@id="pnModalBtn1"]')
                        # go back
                        self.click('//i[@id="styleSJellyBean"]')
                        row['paste_status'] = 'pasted'
                except Exception as e:
                    print('something went wrong', e)
                    row['paste_status'] ='error'
    
        

def test_create_appointment():
    automation = Automation()
    # automation.execute()
    # automation.extract_vitals('MostRecentVitals')
    # automation.extract_vitals('Medications')

    # THIS COULD BE OUR THREAD TO HANDLE POPUPS EVERY SECOND
    monitor_thread = threading.Thread(target=automation.handle_popup_thread)
    monitor_thread.daemon = True
    monitor_thread.start()

    #people = ['carpenter, diana', 'jones, nancy', 'shu, edna', 'thompson, linda']
    people = ['carpenter, diana', 'jones, nancy']
    for person in people:
        automation.createAppointment(person, '08/23/2024')

    automation.hour = 1
    for person in people:
        automation.createAppointment(person, '08/24/2024')

def test_proceed():
    print('starting populating medical history')
    automation = Automation()
    automation.populate_records()

def create_appointment():
    print('starting create appointment')
    store = read()
    automation = Automation()
    
    # THIS COULD BE OUR THREAD TO HANDLE POPUPS EVERY SECOND
    monitor_thread = threading.Thread(target=automation.handle_popup_thread)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    for row in store:
        try:
            appt_type = row['appointment_type']
            if appt_type.lower() != 'f':
                continue
            name = row['name']
            date = row['appt_date']
            parts = name.split(' ')
            parts.pop()
            name = ' '.join(parts)
            
            print(name, date)
            
            date = datetime.strptime(date, "%m/%d/%Y").strftime("%m/%d/%Y")
            print('creating appointment for', name, 'at', date)
            automation.createAppointment(name,date)
            row['appt_status'] = 'created'
        except Exception as e:
            print('something went wrong', e)
            row['appt_status'] = 'error'
            continue


def populate_records():
    automation = Automation()
    
    # THIS COULD BE OUR THREAD TO HANDLE POPUPS EVERY SECOND
    monitor_thread = threading.Thread(target=automation.handle_popup_thread)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    store = read()
    try:
        automation.populate_records(store)
    except Exception as e:
        write(store)
                
        
    
    

#create_appointment()
populate_records()
time.sleep(30)
