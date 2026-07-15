import json
from xmlrpc import client

from auth import get_client
from behavior_modification import get_medications_info
from constants import GOOGLE_SHEET_KEY_BEHAVIORAL_FOSTER_INTAKE, GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_SHELTER_LUV, GOOGLE_SHEET_KEY_SLACK
from fastapi import FastAPI
from google.oauth2.service_account import Credentials
import gspread
from fastapi import Response

from foster_questionnaire_responses import get_foster_notes_questionaire_info_reviewer_expanded
from intake import get_intake_info
from slack import get_slack_info

app = FastAPI()

# @app.get("/foster/{dog_name}")


# @app.get("/medications/{dog_name}")


@app.get("/dog/{dog_name}")
def get_dog_info(dog_name:str):
    slack_info = get_slack_info(dog_name)
    intake_info = get_intake_info(dog_name)
    reviewer_info = get_foster_notes_questionaire_info_reviewer_expanded(dog_name)
    medications_info = get_medications_info(dog_name)
    if not medications_info:
        medications_info = "NONE"
    data = {
        "intake_info": intake_info,
        "reviewer_info": reviewer_info,
        "behavior_updates_slack": slack_info,
        "medications_info": medications_info,
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
