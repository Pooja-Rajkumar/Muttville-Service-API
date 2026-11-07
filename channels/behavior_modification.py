from helpers.constants import GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, MEDICATIONS_WORKSHEET_NAME, MEDS_COLUMN_NAME, TRAINER_COLUMN_NAME, TRAINER_WORKSHEET_ID
from auth.google_sheet_connector import find_google_sheet_matching_records, get_google_sheet, retrieve_google_sheet_records_by_id, retrieve_google_sheet_records_by_name

## The big question - does the dog have behavioral issues? If so, what have we done to address them?
## Send back if we medicated dog for any issues 
def get_medications_info(dog_name: str):
    # aggregate medications info from google sheet once workflow is up 
    records = retrieve_google_sheet_records_by_name(
        GOOGLE_SHEET_KEY_MEDICATIONS, MEDICATIONS_WORKSHEET_NAME
    )
    matched_records = find_google_sheet_matching_records(records, MEDS_COLUMN_NAME, dog_name)
    return matched_records

# Did we get a trainer? Did trainer do anything to fix the behavional issues? 
def get_trainer_response(dog_name: str):
    records = retrieve_google_sheet_records_by_id(
        GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, TRAINER_WORKSHEET_ID
    )
    matched_records = find_google_sheet_matching_records(records, TRAINER_COLUMN_NAME, dog_name)
    return matched_records

