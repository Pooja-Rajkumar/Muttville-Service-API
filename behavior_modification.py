from constants import GOOGLE_SHEET_KEY_MEDICATIONS
from google_sheet_connector import get_google_sheet


def get_medications_info(dog_name: str):
    # aggregate medications info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MEDICATIONS)
    sheet_data = sheet.worksheet("Form Responses 1").get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Dog's name"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info