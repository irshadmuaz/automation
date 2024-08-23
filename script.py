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
            print('text: ' + element.text)
            try:
                element.click()
                
                return
            except:
                continue
    
    def execute(self):
        self.driver.get('https://google.com')
        self.click('//button[@data-event="attributeName"]')
        self.click('//a[@class="thumbnailTitle "]')
        time.sleep(100)

Automation().execute()