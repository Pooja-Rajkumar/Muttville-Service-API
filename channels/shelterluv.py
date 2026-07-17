from constants import GOOGLE_SHEET_KEY_SHELTER_LUV
from google_sheet_connector import get_google_sheet


def get_shelter_luv_info():
    # aggregate shelter luv info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_SHELTER_LUV)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    # Process shelter luv info
    pass