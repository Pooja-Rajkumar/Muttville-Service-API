from enum import Enum

from models.behavior_event import BehaviorEvent

class MedicationStatus(str, Enum):
    APPROVED = "Approved"
    FILLED = "Filled"
    FOSTER_NOTIFIED = "Foster notified"
    READY_FOR_HQ = "Ready for HQ"


class MedicationBehaviorEvent(BehaviorEvent):
    medication: str | None = None
    status: list[MedicationStatus] = []

class TrainerBehaviorEvent(BehaviorEvent):
    trainer_name: str | None = None
    referral_date: str 
    notes: str | None = None