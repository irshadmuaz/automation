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
    
    def click(self,xpath, driver):
        if not driver:
            driver = self.driver
        elements = WebDriverWait(driver, 100).until(lambda x:x.find_elements(By.XPATH, xpath))
        for element in elements:
            try:
                element.click()
                return
            except:
                continue
    
    def new_tab(self):
        newdriver = webdriver.Chrome(service=self.service)
        newdriver.get('https://google.com')
        searchbox = newdriver.find_element(By.CLASS_NAME, "gLFyf")
        searchbox.send_keys('let go on an adventure' + Keys.ENTER)
    
    def execute(self):
        self.driver.get('https://google.com')
        self.new_tab()
        searchbox = self.driver.find_element(By.CLASS_NAME, "gLFyf")
        searchbox.send_keys('let go home' + Keys.ENTER)
        #self.click('//button[@data-event="attributeName"]')
        #self.click('//a[@class="thumbnailTitle "]')
        time.sleep(100)

Automation().execute()