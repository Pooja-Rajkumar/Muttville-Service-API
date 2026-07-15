from constants import GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER_INTAKE
from google_sheet_connector import get_google_sheet


def get_intake_info(dog_name: str):
    # aggregate behavioral info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER_INTAKE)
    sheet_data = sheet.worksheet("Dog Tracker").get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Dog Name"].lower() == dog_name.lower():
            pup_info.append(row)
    # Add here if we want to include trainer info from behavioral foster intake sheet
    return pup_info
