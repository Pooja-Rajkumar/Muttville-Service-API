from helpers.constants import GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER
from auth.google_sheet_connector import get_google_sheet, retrieve_google_records_by_name

def get_intake_info(dog_name: str):
    # aggregate behavioral info from google sheet once workflow is up 
    records = retrieve_google_records_by_name(GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER, "Dog Tracker")
    pup_info = []
    for row in records:
        sl_status = str(row.get("SL Status", "")).strip().lower()
        if row["Dog Name"].lower() == dog_name.lower() and sl_status != "adopted":
            pup_info.append(row)
    return pup_info
