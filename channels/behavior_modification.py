from constants import GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET
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

# Did we get a trainer? Did trainer do anything to fix the behavional issues? 
def get_trainer_response(dog_name: str):
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET)
    tab_id = 1665262541
    sheet_data = sheet.get_worksheet_by_id(tab_id).get_all_records()
    pup_info = []
    trainer_response = {}
    for row in sheet_data: 
        if row["Dog Name"].lower() == dog_name.lower():
            pup_info.append(row)
    return trainer_response

