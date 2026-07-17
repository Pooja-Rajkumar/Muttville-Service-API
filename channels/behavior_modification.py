from constants import GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER, GOOGLE_SHEET_KEY_MEDICATIONS
from google_sheet_connector import get_google_sheet


## The big question - does the dog have behavioral issues? If so, what have we done to address them?
## Send back if we medicated dog for any issues 
def get_medications_info(dog_name: str):
    # aggregate medications info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MEDICATIONS)
    sheet_data = sheet.worksheet("Form Responses 1").get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Dog's name"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info

## Did foster do anything to fix the behavional issues?
def get_foster_response(dog_name: str):
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER)
    sheet_id = 0 # Dog Tracker tab
    sheet_data = sheet.worksheet(sheet_id).get_all_records()
    pup_info = []
    foster_response = {}
    for row in sheet_data:
        if row["Dog name"].lower() == dog_name.lower():
            pup_info.append(row)
    for row in pup_info:
        if row["Foster response"] != "":
            foster_response["Foster response"] = row["Foster response"]
        if row["Foster response date"] != "":
            foster_response["Foster response date"] = row["Foster response date"]   
    return foster_response

# Did trainer do anything to fix the behavional issues?
def get_trainer_response(dog_name: str):
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER)
    sheet_id = 0 # Dog Tracker tab
    sheet_data = sheet.worksheet(sheet_id).get_all_records()
    pup_info = []
    trainer_response = {}
    for row in sheet_data:
        if row["Dog name"].lower() == dog_name.lower():
            pup_info.append(row)
    for row in pup_info:
        if row["Trainer response"] != "":
            trainer_response["Trainer response"] = row["Trainer response"]
        if row["Trainer response date"] != "":
            trainer_response["Trainer response date"] = row["Trainer response date"]   
    return trainer_response

