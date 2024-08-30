import time
from filereader import read, write
from parsers import parse_name, parse_records

def set_vitals_box(automation,xpath, text):
    # click vitals
    automation.click('//b[@onclick="pnSectionClicked(\'Vitals:\', event)"]')
    print('looking for iframe')
    automation.switch_to_frame(xpath)
    body = automation.find('//body')
    print('found iframe body', body.text)
    body.clear()
    body.send_keys(text)
    print('pasted vitals')
    automation.driver.switch_to.default_content()

# patient name, vitals and medication when on patients list page
def fill_appointment(automation, name, vitals):
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
            set_vitals_box(automation,'//iframe[@class="wysihtml5-sandbox managed-iframe hk-iframe"]', vitals)
            # close modal
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
            vitals = parse_records(row['vitals'])
            if appt_type != f or paste_status in ('done', 'error'):
                print('skipping', name, 'pasted:', paste_status, 'appt:', appt_type)
                continue
            fill_appointment(automation,name,vitals)
            row['paste_status'] = 'done'
        except:
            print('some thing went wrong')
            row['paste_status']='error'
            automation.driver.refresh()
        finally:
            # go back to appointment list
            automation.click('//i[@id="styleSJellyBean"]')
    write(store)

