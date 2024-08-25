from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait 
import time

class Automation:
    def __init__(self):
        self.service = Service('chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service)
    
    def click(self,xpath):
        elements = WebDriverWait(self.driver, 100).until(lambda x:x.find_elements(By.XPATH, xpath))
        for element in elements:
            try:
                element.click()
                return
            except:
                continue
    
    def find(self, xpath):
        return WebDriverWait(self.driver, 100).until(lambda x:x.find_element(By.XPATH, xpath))
    
    def sendkeys(self, element, keys):
        element.send_keys(keys + Keys.ENTER)
    
    def execute(self):
        # Go to point click 
        self.driver.get('https://pointclickcare.com/')
        # Click login
        self.click('//span[@class="menu-text"]')

        # variable
        name = "jones nancy"
        element = self.find('//input[@id="searchField"]')
        element.send_keys(name + Keys.ENTER)

        #todo copy medications and vitals
    
    def eclinic(self):
        self.driver.get('https://caazadhaw3mrvlx9ayapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp#/mobiledoc/jsp/webemr/jellybean/officevisit/officeVisits.jsp')
        self.click('//a[@id="jellybean-panelLink65"]')
        searchbox = self.find('//input[@id="searchText"]')
        #variable
        name = "carpenter, diana"
        self.sendkeys(searchbox, name)
        time.sleep(1)
        self.click('//span[@id="patientLName1"]')

        #patientLName1
        time.sleep(100)
    
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
automation.extract_vitals('MostRecentVitals')
automation.extract_vitals('Medications')
