from automation import Automation
from create_appointment import create_all_appointments, createAppointment
from populate_appointment import fill_all_appointments, fill_appointment
from extract_pointclick import copy_all_vitals, copy_vitals, extract_vitals
def execute():
    automation = Automation()

    # copy_all_vitals()
    # create_all_appointments()
    # fill_all_appointments()

    found = extract_vitals(automation,'Medications')
    print(found)

execute()



    
