from automation import Automation
from create_appointment import create_all_appointments, createAppointment, followAppointment
from populate_appointment import fill_all_appointments, fill_appointment, set_iframe_box,copy_encounters,add_assessment
from extract_pointclick import copy_all_vitals, copy_vitals, extract_vitals
import sys
from datetime import datetime, timedelta
import time
def execute():
    automation = Automation()
    command = sys.argv[1]
    # copy_all_vitals()
    # create_all_appointments()
    #fill_all_appointments(automation)

    #fill_appointment(automation, 'Carpenter, Diana', 'vitals', 'medication')
    #followAppointment(automation, '08/28/2024', 'headache')
    if (command == 'pointclick'):
        copy_all_vitals(automation)
    elif (command == 'appointment'):
        automation.start_thread()
        create_all_appointments(automation)
    elif (command == 'fill'):
        automation.start_thread()
        fill_all_appointments(automation)
    elif (command == 'appointment+fill'):
        automation.start_thread()
        create_all_appointments(automation)
        time.sleep(1)
        automation.driver.refresh()
        time.sleep(1)
        fill_all_appointments(automation)

        
    elif (command == 'test'):
        # date = '09/20/2024'
        # formatted = datetime.strptime(date, "%m/%d/%Y").strftime("%m/%d/%Y")
        # followAppointment(automation, formatted, 'reason', 'roseville care')
        copy_encounters(automation)



execute()



    
