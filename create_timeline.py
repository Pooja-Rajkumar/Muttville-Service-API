import json

from channels.behavior_modification import get_medications_info, get_trainer_response
from channels.foster_questionnaire_responses import get_foster_notes_questionaire_info_reviewer_expanded
from channels.intake import get_intake_info
from channels.slack import get_slack_info

# Gather behavior specific queries about dog 
def get_behavior_info(dog_name: str):
    medications_info = get_medications_info(dog_name)
    trainer_response = get_trainer_response(dog_name)
    behavior_modifications = []
    behavior_modifications.append(medications_info)
    behavior_modifications.append(trainer_response)
    return behavior_modifications

## Aggregate dog information and create a timeline of events for a given dog.
def get_dog_info(dog_name:str):
    slack_info = get_slack_info(dog_name)
    intake_info = get_intake_info(dog_name)
    foster_info = get_foster_notes_questionaire_info_reviewer_expanded(dog_name)
    behavior_info = get_behavior_info(dog_name)
    data = {
        "intake_info": intake_info,
        "foster_info": foster_info,
        "behavior_updates_slack": slack_info,
        "behavior_info": behavior_info,
    }
    return data

def create_timeline(dog_name:str):
    dog_info = get_dog_info(dog_name)
    print(f"Dog Info: {json.dumps(dog_info, indent=2)}")