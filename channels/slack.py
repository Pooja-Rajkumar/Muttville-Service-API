from constants import GOOGLE_SHEET_KEY_SLACK
from google_sheet_connector import get_google_sheet


def get_slack_info(dog_name: str):
    # aggregate slack info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_SLACK)
    sheet_data = sheet.worksheet("Form Responses").get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Pup Name"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info