from helpers.constants import GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET
from auth.google_sheet_connector import find_matching_records, get_google_sheet, retrieve_google_records_by_id, retrieve_google_records_by_name

## The big question - does the dog have behavioral issues? If so, what have we done to address them?
## Send back if we medicated dog for any issues 
def get_medications_info(dog_name: str):
    # aggregate medications info from google sheet once workflow is up 
    records = retrieve_google_records_by_name(
        GOOGLE_SHEET_KEY_MEDICATIONS, "Form Responses 1"
    )
    matched_records = find_matching_records(records, "Dog's name", dog_name)
    return matched_records

# Did we get a trainer? Did trainer do anything to fix the behavional issues? 
def get_trainer_response(dog_name: str):
    records = retrieve_google_records_by_id(
        GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, 1665262541
    )
    matched_records = find_matching_records(records, "Dog Name", dog_name)
    return matched_records

