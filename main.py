from fastapi import FastAPI
from google.oauth2.service_account import Credentials
import sys
import gspread


app = FastAPI()


def get_google_sheet():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES,
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1BOK-EnSoYVmEV9uKYl4PWynJk2jXRP5wZOfYiRG6Saw")
    return sheet

def get_slack_info():
    # aggregate slack info from google sheet once workflow is up 
    pass

@app.get("/dog/{dog_name}")
def get_dog_info(dog_name:str):
    sheet = get_google_sheet()
    worksheet = sheet.get_worksheet(0)
    sheet_data = worksheet.get_all_records()
    for row in sheet_data:
        if row["Mutt's Name"].lower() == dog_name.lower():
            return row

def main():
    print("Hello from muttville-service-api!")


if __name__ == "__main__":
    main()
