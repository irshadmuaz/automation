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
            self.tryClick('//button[@data-bb-handler="confirm"]')
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
        
    def tryClick(self, xpath):
        try:
            self.click(xpath, 10)
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




#automation.followAppointment()
time.sleep(30)
