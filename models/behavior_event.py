from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, computed_field

class BehaviorConcern(str, Enum):
    LEASH_REACTIVITY = "Leash Reactivity"
    SEPARATION_DISTRESS = "Separation Distress"
    HANDLING_SENSITIVITY = "Handling Sensitivity"
    RESOURCE_GUARDING = "Resource Guarding"
    POTTY_TRAINING = "Potty Training"
    INTROS_TO_RESIDENT_PET = "Intros to Resident Pet"
    OTHER = "Other"

class EventSource(str, Enum):
    GS_MEDICATIONS = "Medications"
    GS_MUTT_CHEAT_SHEET = "Mutt Cheat Sheet"
    GS_FOSTER_QUESTIONNAIRE = "Foster Questionnaire"
    GS_BEHAVIORAL_OUTREACH_FOSTER = "Behavioral Outreach Foster"
    SLACK_BEHAVIOR_UPDATES = "Behavior Updates"
    MANUAL = "Manual Entry"

class BehaviorEvent(BaseModel):
    timestamp: datetime
    
    @computed_field
    @property
    def timestamp_display(self) -> str:
        return self.timestamp.strftime("%b %d, %Y • %I:%M %p")

    inputted_by: str | None = None
    dog_name: str
    source: EventSource
    concerns: list[BehaviorConcern]
    summary: str
    event_id: str # This varies by channel
    location: str | None = None
    # medication: str | None = None
