import json

from constants import GOOGLE_SHEET_KEY, GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER, GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER_INTAKE, GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_SHELTER_LUV, GOOGLE_SHEET_KEY_SLACK
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
    return sheet

@app.get("/behavioral/foster/{dog_name}") # behavioral outreach (foster) = intake
def get_intake_info(dog_name: str):
    # aggregate behavioral info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER_INTAKE)
    sheet_data = sheet.get_worksheet(1).get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Dog Name"].lower() == dog_name.lower():
            pup_info.append(row)
    # Add here if we want to include trainer info from behavioral foster intake sheet
    return pup_info


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
def get_foster_notes_questionaire_info_reviewer_expanded(dog_name: str):
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE)
    sheet_data = sheet.get_worksheet(2).get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Mutt's Name"].lower() == dog_name.lower():
            pup_info.append(row)
    return pup_info

@app.get("/medications/{dog_name}")
def get_medications_info(dog_name: str):
    # aggregate medications info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MEDICATIONS)
    sheet_data = sheet.get_worksheet(0).get_all_records()
    pup_info = []
    for row in sheet_data:
        if row["Dog's Name"].lower() == dog_name.lower():
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
    intake_info = get_intake_info(dog_name)
    reviewer_info = get_foster_notes_questionaire_info_reviewer_expanded(dog_name)
    medications_info = get_medications_info(dog_name)
    if not medications_info:
        medications_info = "NONE"
    # shelter_luv_info = get_shelter_luv_info()  # Uncomment when implemented
    data = {
        "intake_info": intake_info,
        "reviewer_info": reviewer_info,
        "behavior_updates_slack": slack_info,
        "medications_info": medications_info,
        # "shelter_luv_info": shelter_luv_info,  # Uncomment when implemented
    }
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
    )

def create_story():
    # Function to create a story based on the aggregated information
    pass

def main():
    print("Hello from muttville-service-api!")


if __name__ == "__main__":
    main()
