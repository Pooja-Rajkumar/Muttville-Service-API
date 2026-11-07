from helpers.constants import FOSTER_QUESTIONNAIRE_COLUMN_NAME, FOSTER_QUESTIONNAIRE_WORKSHEET_ID, GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE
from auth.google_sheet_connector import find_google_sheet_matching_records, get_google_sheet, retrieve_google_sheet_records_by_id


def get_foster_notes_questionaire_info_reviewer_expanded(dog_name: str):
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    records = retrieve_google_sheet_records_by_id(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, FOSTER_QUESTIONNAIRE_WORKSHEET_ID)
    pup_info = find_google_sheet_matching_records(records, FOSTER_QUESTIONNAIRE_COLUMN_NAME, dog_name)
    return pup_info