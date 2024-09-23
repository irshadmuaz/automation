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
    
    def click(self,xpath, wait=100):
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
            
    def findOf(self, element, xpath, wait=100):
        return WebDriverWait(element, wait).until(lambda x:x.find_element(By.XPATH, xpath))
    
    def find(self, xpath, wait=100):
        return WebDriverWait(self.driver, wait).until(lambda x:x.find_element(By.XPATH, xpath))
    
    def find_all(self, xpath, wait=100):
        return WebDriverWait(self.driver, wait).until(lambda x:x.find_elements(By.XPATH, xpath))
    
    def tryClick(self, xpath, wait=10):
        try:
            self.click(xpath, wait)
            print('successfully closed popup ' + xpath, str(datetime.datetime.now()))
        except: 
            return
    
    def start_thread(self):
        monitor_thread = threading.Thread(target=self.handle_popup_thread)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def scroll_to(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)

    def sendkeys(self, element, keys):
        element.send_keys(keys + Keys.ENTER)
    
    def switch_to_frame(self, xpath):
        iframe = self.find(xpath)
        print('found iframe', iframe)
        self.driver.switch_to.frame(iframe)
        print('switched to iframe')
    