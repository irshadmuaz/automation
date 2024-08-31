import time
from filereader import read, write
from parsers import parse_name, parse_records

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

# patient name, vitals and medication when on patients list page
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
            
            # click vitals
            automation.click('//b[@onclick="pnSectionClicked(\'Vitals:\', event)"]')
            set_iframe_box(automation, vitals)
            # close modal
            automation.click('//button[@id="pnModalBtn1"]')
            time.sleep(1)
            
            automation.click('//b[@onclick="pnSectionClicked(\'ROS:\', event)"]')
            set_iframe_box(automation, medication)
            automation.click('//button[@id="pnModalBtn1"]')
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
            automation.driver.refresh()
            time.sleep(5)
        finally:
            # go back to appointment list
            automation.click('//i[@id="styleSJellyBean"]')
    
    print('Filled all appointments')
    write(store)

