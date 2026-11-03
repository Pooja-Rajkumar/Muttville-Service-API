from helpers.constants import GOOGLE_SHEET_KEY_SLACK
from auth.google_sheet_connector import find_matching_records, get_google_sheet, retrieve_google_records_by_name


def get_slack_info(dog_name: str):
    # aggregate slack info from google sheet once workflow is up 
    records = retrieve_google_records_by_name(GOOGLE_SHEET_KEY_SLACK, "Form Responses")
    pup_info = find_matching_records(records, "Pup Name", dog_name)
    return pup_info