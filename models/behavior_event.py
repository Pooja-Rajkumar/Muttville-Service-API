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
    GS_MEDICATIONS = "Google Sheet - Medications"
    GS_MUTT_CHEAT_SHEET = "Google Sheet - Mutt Cheat Sheet"
    GS_FOSTER_QUESTIONNAIRE = "Google Sheet - Foster Questionnaire"
    GS_BEHAVIORAL_OUTREACH_FOSTER = "Google Sheet - Behavioral Outreach Foster"
    SLACK_BEHAVIOR_UPDATES = "Slack - Behavior Updates"

class BehaviorEvent(BaseModel):
    occurred_at: datetime
    
    @computed_field
    @property
    def occurred_at_display(self) -> str:
        return self.occurred_at.strftime("%b %d, %Y • %I:%M %p")
    
    dog_name: str
    source: EventSource
    concern: list[BehaviorConcern]
    summary: str

    details: dict | None = None
    location: str | None = None
    medication: str | None = None

    raw_data: dict = Field(default_factory=dict)