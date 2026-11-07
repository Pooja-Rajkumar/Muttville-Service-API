from helpers.constants import ADOPTED, ADOPTED, FOSTER_QUESTIONNAIRE_COLUMN_NAME, FOSTER_QUESTIONNAIRE_WORKSHEET_ID, GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, TRAINER_COLUMN_NAME, GOOGLE_SHEET_KEY_MEDICATIONS
from auth.google_sheet_connector import find_google_sheet_matching_records, get_google_sheet, retrieve_google_sheet_records_by_id, retrieve_google_sheet_records_by_name
from models.channel_model import GoogleSheetSource, Shelter

def get_google_sheet_records(metadata: GoogleSheetSource, dog_name: str, search_by_id: bool = False):
    if search_by_id:
        records = retrieve_google_sheet_records_by_id(metadata.sheet_key, metadata.worksheet_id)
    else:
        records = retrieve_google_sheet_records_by_name(metadata.sheet_key, metadata.worksheet_name)
    
    matched_records = find_google_sheet_matching_records(records, metadata.desired_column_name, dog_name)

    return matched_records
