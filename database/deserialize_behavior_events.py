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
    "IntakeEvent": IntakeEvent,
}

def deserialize_behavior_event(row):
    event_model = EVENT_MODELS[row["event_type"]]

    event_data = json.loads(row["event_data"])
    concerns = json.loads(row["concerns"])

    return event_model(
        occurred_at=row["occurred_at"],
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