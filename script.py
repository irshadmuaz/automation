from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait 
import datetime
import time
import json


class Automation:
    def __init__(self):
        self.service = Service('chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.window_handles
        self.hour = 1
    
    def click(self,xpath, wait=1000):
        elements = WebDriverWait(self.driver, wait).until(lambda x:x.find_elements(By.XPATH, xpath))
        for element in elements:
            try:
                element.click()
            except:
                continue
    
    def get_time(self):
        return '0{0}:00 pm'.format(self.hour)
        self.hour+=1
    
    def save_cookies(self):
        cookies = self.driver.get_cookies()
        # Store cookies in a file
        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)
    
    def get_url(self, url):
        #cookies = {}
        #with open('cookies.json', 'r') as file:
            #cookies = json.load(file)

        # Goto the same URL
        self.driver.get(url)

        # Set stored cookies to maintain the session
        #for cookie in cookies:
            #self.driver.add_cookie(cookie)
    
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
        
    def tryClick(self, xpath):
        try:
            self.click(xpath, 10)
            print('successfully closed popup ' + xpath, str(datetime.datetime.now()))
        except: 
            return
        
    def eclinic(self):
        self.get_url('https://caazadhaw3mrvlx9ayapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp#/mobiledoc/jsp/webemr/jellybean/officevisit/officeVisits.jsp')
        
    
    def createAppointment(self, name):
        #self.driver.get('file:///C:/Users/abdul/Documents/GitHub/automation/pages/createappointment.html')
        #self.save_cookies()
        self.click('//a[@id="jellybean-panelLink65"]')
        #variable
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
        time.sleep(5)
        self.tryClick('//button[@id="billingAlertBtn6"]')

        #click autocomplete follow up
        self.click('//input[@id="visit-type-lookupIpt1"]')

        # select follow up
        self.click('//a[@id="visit-type-lookupLink1ngR12"]')

        #set date
        # try:
        #     print('attempting to set date')
        #     datebox = self.find('//input[@id="Appt_startDate"]')
        #     datebox.send_keys('08/27/2024' + Keys.ENTER)
        #     time.sleep(1)
        #     timestart = self.find('//input[@id="time-lookup_timeLookup2788_Ipt1"]')
        #     timeend = self.find('//input[@id="time-lookup_timeLookup0232_Ipt1"]')
        #     timestart.send_keys(self.get_time() + Keys.ENTER)
        #     timeend.send_keys(self.get_time() + Keys.ENTER)
        #     print('set time and date')
        # except:
        #     print('something went wrong here')


        # click ok
        self.click('//button[@id="newAppointmentBtn51"]')
        print('clicked ok to create appointment')

        # try dismiss popup
        self.tryClick('//button[@data-bb-handler="confirm"]')
        # try dismiss second popup
        time.sleep(5)
        self.tryClick('//button[@data-bb-handler="confirm"]')
        

        # close patient modal
        self.click('//button[@id="patient-hubBtn1"]')
        print('closed appointment modal')
        time.sleep(5)
    
    def extract_vitals(self, iframeName):
        #self.driver.get('file:///C:/Users/irsha/Documents/Github/selenium/dash.html')
        vitals_frame = self.find('//iframe[@name="{0}"]'.format(iframeName))
        self.driver.switch_to.frame(vitals_frame)

        cols = self.driver.find_elements(By.XPATH,'//td[@class="detailColHeader"]')
        columns = [c.text for c in cols]
        rows = [columns]
        tablerows = self.driver.find_elements(By.XPATH, '//tr[@class="normalRow"]')
        for row in tablerows:
            rows.append([c.text for c in row.find_elements(By.TAG_NAME, 'td')])
        
        for row in rows:
            print(row)

        self.driver.switch_to.default_content()


automation = Automation()
# automation.execute()
# automation.extract_vitals('MostRecentVitals')
# automation.extract_vitals('Medications')

automation.eclinic()
automation.createAppointment('carpenter, diana')
automation.createAppointment('jones, nancy')
automation.createAppointment('shu, edna')
automation.createAppointment('thompson, linda')
