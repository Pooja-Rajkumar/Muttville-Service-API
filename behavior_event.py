from datetime import datetime
from enum import Enum

class BehaviorEvent:
    date: datetime
    source: str
    category: str
    summary: str
    details: dict

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
    GS_FOSTER_QUESTIONAIRE = "Google Sheet - Foster Questionnaire"
    GS_BEHAVIORAL_OUTREACH_FOSTER = "Google Sheet - Behavioral Outreach Foster"
    SLACK_BEHAVIOR_UPDATES = "Slack - Behavior Updates"

# doubtful we will need this 
# class EventType(str, Enum):
#     BEHAVIOR = "Behavior"
#     MEDICATION = "Medication"
#     TRAINING = "Training"
#     ADOPTION = "Adoption"

# class Severity(str, Enum):
#     LOW = "Low"
#     MEDIUM = "Medium"
#     HIGH = "High"