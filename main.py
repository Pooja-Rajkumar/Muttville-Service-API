import json
from xmlrpc import client

from channels.behavior_modification import get_medications_info, get_trainer_response
from fastapi import FastAPI
from google.oauth2.service_account import Credentials
import gspread
from fastapi import Response

from channels.foster_questionnaire_responses import get_foster_notes_questionaire_info_reviewer_expanded
from channels.intake import get_intake_info
from channels.slack import get_slack_info
from create_timeline import create_timeline

app = FastAPI()

# @app.get("/foster/{dog_name}")


@app.get("/behavior/{dog_name}")
def get_behavior_info(dog_name: str):
    medications_info = get_medications_info(dog_name)
    # trainer_response = get_trainer_response(dog_name)
    data = {
        "medications_info": medications_info,
        #"foster_response": foster_response,
        # "trainer_response": trainer_response,
    }
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
    )


@app.get("/dog/{dog_name}")
def get_dog_info(dog_name:str):
    data = create_timeline(dog_name)
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
