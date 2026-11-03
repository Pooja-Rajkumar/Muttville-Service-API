from helpers.constants import GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE
from auth.google_sheet_connector import find_matching_records, get_google_sheet, retrieve_google_records_by_id


def get_foster_notes_questionaire_info_reviewer_expanded(dog_name: str):
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    target_sheet_id = 637846814 # Reviewer View (Expanded) tab
    records = retrieve_google_records_by_id(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, target_sheet_id)
    pup_info = find_matching_records(records, "Mutt's Name", dog_name)
    return pup_info