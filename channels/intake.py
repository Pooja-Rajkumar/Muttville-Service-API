from helpers.constants import ADOPTED, GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER, INTAKE_COLUMN_NAME, INTAKE_WORKSHEET_NAME
from auth.google_sheet_connector import get_google_sheet, retrieve_google_sheet_records_by_name
from models.channel_model import GoogleSheetSource

def get_intake_info(dog_name: str):
    # aggregate behavioral info from google sheet once workflow is up 
    records = retrieve_google_sheet_records_by_name(GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER, INTAKE_WORKSHEET_NAME)
    pup_info = []
    for row in records:
        sl_status = str(row.get("SL Status", "")).strip().lower()
        if row[INTAKE_COLUMN_NAME].lower() == dog_name.lower() and sl_status != ADOPTED:
            pup_info.append(row)
    return pup_info

# muttville specific getter for intake records because we need to do an extra filter check 
def get_google_sheet_intake_records(metadata: GoogleSheetSource, dog_name: str):
    # aggregate behavioral info from google sheet once workflow is up 
    records = retrieve_google_sheet_records_by_name(metadata.sheet_key, metadata.worksheet_name)
    pup_info = []
    for row in records:
        sl_status = str(row.get("SL Status", "")).strip().lower()
        if row[metadata.desired_column_name].lower() == dog_name.lower() and sl_status != ADOPTED:
            pup_info.append(row)
    return pup_info
