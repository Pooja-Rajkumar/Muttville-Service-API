from typing import Dict, List

from auth.auth import get_client


def get_google_sheet(key: str):
    client = get_client()
    sheet = client.open_by_key(key)
    return sheet


def retrieve_google_sheet_records_by_name(sheet_key: str, worksheet_name: str):
    print("Retrieve google sheet records by name")
    sheet = get_google_sheet(sheet_key)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet.get_all_records() 

def retrieve_google_sheet_records_by_id(sheet_key: str, worksheet_id: int):
    print("Retrieve google sheet records by id")
    sheet = get_google_sheet(sheet_key)
    worksheet = sheet.get_worksheet_by_id(worksheet_id)
    return worksheet.get_all_records()

def find_google_sheet_matching_records(sheet_data: List[Dict[str, int | float | str]], column_name:str, dog_name: str):
    pup_info = []
    for row in sheet_data: 
        if row[column_name].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info