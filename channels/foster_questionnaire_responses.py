
from constants import GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE
from google_sheet_connector import get_google_sheet


def get_foster_notes_questionaire_info_reviewer_expanded(dog_name: str):
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE)
    target_sheet_id = 637846814 # Reviewer View (Expanded) tab
    worksheet = sheet.get_worksheet_by_id(target_sheet_id)
    print(f"Confirmed: Reading from tab '{worksheet.title}'")
    sheet_data = worksheet.get_all_records()

    pup_info = []
    for row in sheet_data:
        if row["Mutt's Name"].lower() == dog_name.lower():
            pup_info.append(row)
    
    return pup_info