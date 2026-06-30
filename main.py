import json

from constants import GOOGLE_SHEET_KEY, GOOGLE_SHEET_KEY_SHELTER_LUV, GOOGLE_SHEET_KEY_SLACK
from fastapi import FastAPI
from google.oauth2.service_account import Credentials
import gspread
from fastapi import Response

app = FastAPI()


def get_google_sheet(key: str):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(key)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    print(f"{key} info:", sheet_data)
    return sheet

@app.get("/slack/{dog_name}")
def get_slack_info(dog_name: str):
    # aggregate slack info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_SLACK)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    print(f"{GOOGLE_SHEET_KEY_SLACK} info:", sheet_data)
    pup_info = []
    for row in sheet_data:
        if row["title"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info

@app.get("/foster/{dog_name}")
def get_foster_notes_questionaire_info(dog_name: str):
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Mutt's Name"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info

def get_shelter_luv_info():
    # aggregate shelter luv info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_SHELTER_LUV)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    print(f"{GOOGLE_SHEET_KEY_SHELTER_LUV} info:", sheet_data)
    # Process shelter luv info
    pass

@app.get("/dog/{dog_name}")
def get_dog_info(dog_name:str):
    slack_info = get_slack_info(dog_name)
    foster_info = get_foster_notes_questionaire_info(dog_name)
    # shelter_luv_info = get_shelter_luv_info()  # Uncomment when implemented
    data = {
        "behavior_updates_slack": slack_info,
        "foster_questionnaire_profile": foster_info,
        # "shelter_luv_info": shelter_luv_info,  # Uncomment when implemented
    }
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
    )

def main():
    print("Hello from muttville-service-api!")


if __name__ == "__main__":
    main()
