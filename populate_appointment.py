import time
from filereader import read, write
from parsers import parse_name, parse_records
from selenium.webdriver.common.by import By
import re

# finds the iframe and sends text to it
def set_iframe_box(automation, text):
    print('looking for iframe')
    automation.switch_to_frame('//iframe[@class="wysihtml5-sandbox managed-iframe hk-iframe"]')
    body = automation.find('//body')
    print('found iframe body', body.text)
    body.clear()
    body.send_keys(text)
    print('pasted vitals')
    automation.driver.switch_to.default_content()

# patient name, vitals and medication and copy hpi when on patients list page
def fill_appointment(automation, name, vitals, medication):
    elements = automation.find_all("//span[starts-with(@id, 'officeVisitsLink')]")
    dictionary = {}
    for element in elements:
        dictionary[element.text]=element
    for key in dictionary.keys():
        if key.lower().startswith(name.lower()):
            print('found name', name)
            element = dictionary[key]
            automation.scroll_to(element)
            element.click()
            
            if vitals:
                # click vitals
                automation.click('//b[@onclick="pnSectionClicked(\'Vitals:\', event)"]')
                set_iframe_box(automation, vitals)
                # close modal
                automation.click('//button[@id="pnModalBtn1"]')
                time.sleep(1)
            
            if medication:
                automation.click('//b[@onclick="pnSectionClicked(\'ROS:\', event)"]')
                set_iframe_box(automation, medication)
                automation.click('//button[@id="pnModalBtn1"]')
                time.sleep(1)
            
            # copy encounters
            copy_encounters(automation)
            time.sleep(1)
            # go back
            automation.click('//i[@id="styleSJellyBean"]')
            time.sleep(2)

def fill_all_appointments(automation):
    store = read()
    for row in store:
        try:
            name = parse_name(row['name'])
            appt_type = row['appointment_type'].lower()
            paste_status = row['paste_status']
            vitals = parse_records(row['vitals'],1)
            medication = parse_records(row['medication'],3, 'Current medications')
            
            if appt_type != 'f' or paste_status in ('done', 'error'):
                print('skipping', name, 'pasted:', paste_status, 'appt:', appt_type)
                continue
            fill_appointment(automation,name,vitals, medication)
            row['paste_status'] = 'done'
        except Exception as e:
            print('some thing went wrong', e)
            row['paste_status']='error'
            # go back
            automation.click('//i[@id="styleSJellyBean"]')
            time.sleep(2)
            automation.driver.refresh()
            time.sleep(10)
        finally:
            # go back to appointment list
            automation.click('//i[@id="styleSJellyBean"]')
    
    print('Filled all appointments')
    write(store)

def copy_encounters(automation):
    # click encounter
    automation.click('//a[@id="topPanelLink22"]')
    table = automation.find('//*[@id="Encounter-lookupTbl2"]/tbody')
    time.sleep(2)
    rows = table.find_elements(By.XPATH, './tr')
    found = False
    for row in rows:
        date = row.find_element(By.XPATH, './td[@ng-bind="enc.date"]')
        try:
            locked = row.find_element(By.XPATH, './td/i[@class="icon icon-lock"]')
            name = row.find_element(By.XPATH, './td[@ng-bind="enc.doctorname" and @title="Khan, Abdulhalim"]')
            # ATTENTION: use followup as criteria
            if automation.has('./td/span[@title="F/U : Follow Up Visit"]',row):
                followup =  automation.findOf(row,'./td/span[@title="F/U : Follow Up Visit"]')
                followup.click()
            elif automation.has('./td/span[@title="NP : New Patient"]',row):
                np = automation.findOf(row, './td/span[@title="NP : New Patient"]')
                np.click()
            break
            found = True
        except:
            continue

    if not found:
        # close encounters
        automation.click('//button[@id="Encounter-lookupBtn1"]')
        return
    #copy details
    chiefComplaint = automation.find('//table[@prisma-section="HPI"]/tbody/tr[1]/td[2]/div')
    cctext = chiefComplaint.text
    
    ccfixed = ''
    index = cctext.find('ROS:')
    secondindex =cctext.find('ROS:',index+1)
    if secondindex != -1:
        ccfixed = cctext[:secondindex+4]
    else:
        ccfixed = cctext.split('Medical History:')[0].strip()
        
    assessment = automation.find('//table[@prisma-section="Assessment"]')
    asstext = assessment.text
    print(assessment.text)
    #close modal
    automation.click('//*[@id="encounterPreviewApp"]/div/div/div[1]/button')
    time.sleep(1)
    # close encounters
    automation.click('//button[@id="Encounter-lookupBtn1"]')
    time.sleep(2)
    # go to hpi
    automation.click('//a[@ng-click="loadProgressNotePopup(\'HPI:\');"]')
    time.sleep(1)
    automation.click('//a/span/span[@title="Constitutional"]')
    time.sleep(1)
    set_iframe_box(automation, ccfixed)
    automation.click('//button[@id="pnModalBtn1"]')
    time.sleep(2)

    codes = re.findall(r'-\s*([A-Z]\d+\.\d+)', asstext)
    if 'I10' in asstext:
        codes.append('I10')
    print('codes', codes)
    for code in codes:
        add_assessment(automation, code)
        time.sleep(3)
    print('completed pasting hpi and assessment')

def add_assessment(automation, code):
    
    table = automation.find('//table[@id="overview_rpTbl12"]')
    rows = table.find_elements(By.XPATH, './tbody/tr[1]')
    for row in rows:
        try:
            #//*[@id="prolist294075"]/td[4]/div
            #//*[@id="prolist295343"]/td[4]/div
            el = row.find_element(By.XPATH, f'./td/div[@title="{code}"]')
            addbtn = automation.findOf(row,'./td/button[@title="Add problem list to notes"]')
            addbtn.click()
            print('found', code)
            break
        except:
            #print('not found', code)
            continue
    