import json
from channels.behavior_modification import get_medications_info, get_trainer_response
from fastapi import FastAPI
from fastapi import Response
from channels.foster_questionnaire_responses import get_foster_notes_questionaire_info_reviewer_expanded
from channels.intake import get_intake_info
from channels.slack import get_slack_info
from create_timeline import create_timeline
from parsers.behavior_modification_parser import parse_medication_info, parse_trainer_info
from parsers.foster_questionnaire_parser import parse_foster_questionnaire
from parsers.intake_parser import parse_intake_info
from parsers.slack_parser import parse_slack_behavior_updates

app = FastAPI()

# @app.get("/foster/{dog_name}")



@app.get("/dog/{dog_name}")
def get_dog_info(dog_name:str):
    medication_info = get_medications_info(dog_name)
    normalized_medication_info = parse_medication_info(medication_info)
    
    trainer_modifications = get_trainer_response(dog_name)
    normalized_trainer_modifications = parse_trainer_info(trainer_modifications)
    
    foster_questionnaire_info = get_foster_notes_questionaire_info_reviewer_expanded(dog_name)
    normalized_foster_questionnaire_info = parse_foster_questionnaire(foster_questionnaire_info)
    
    intake_info = get_intake_info(dog_name)
    normalized_intake_info = parse_intake_info(intake_info)
    
    slack_info = get_slack_info(dog_name)
    normalized_slack_info = parse_slack_behavior_updates(slack_info)
    
    pass


def create_story():
    # Function to create a story based on the aggregated information
    pass

def main():
    print("Hello from muttville-service-api!")


if __name__ == "__main__":
    main()
