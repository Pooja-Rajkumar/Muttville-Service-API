import json

from models.behavior_event import BehaviorEvent, BehaviorConcern, EventSource
from models.behavior_modification_event import MedicationBehaviorEvent, TrainerBehaviorEvent
from models.foster_behavior_event import FosterBehaviorEvent

from models.intake_event import IntakeEvent


EVENT_MODELS = {
    "BehaviorEvent": BehaviorEvent,
    "FosterBehaviorEvent": FosterBehaviorEvent,
    "MedicationBehaviorEvent": MedicationBehaviorEvent,
    "TrainerBehaviorEvent": TrainerBehaviorEvent,
    "IntakeEvent": IntakeEvent,}

def convert_row_to_event(row):
    event_model = EVENT_MODELS[row["event_type"]] # return the class that we want 

    event_data = json.loads(row["event_data"]) # dump event data into dictionary
    concerns = json.loads(row["concerns"]) # dump concerns into dictionary

    return event_model( # instantiate the class and dump all the extraneous data into the class 
        timestamp=row["timestamp"],
        event_id=row["event_id"],
        inputted_by=row["inputted_by"],
        dog_name=row["dog_name"],
        source=EventSource(row["source"]),
        concerns=[
            BehaviorConcern(concern)
            for concern in concerns
        ],
        summary=row["summary"],
        **event_data,
    )