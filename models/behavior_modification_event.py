from enum import Enum

from models.behavior_event import BehaviorEvent

class MedicationStatus(str, Enum):
    APPROVED = "Approved"
    FILLED = "Filled"
    FOSTER_NOTIFIED = "Foster notified"
    READY_FOR_HQ = "Ready for HQ"
    UNKNOWN = "unknown"  # Your catch-all variant

    @classmethod
    def _missing_(cls, value):
        """Intercepts unknown initialization values and returns the fallback."""
        return cls.UNKNOWN



class MedicationBehaviorEvent(BehaviorEvent):
    medication: str | None = None
    status: list[MedicationStatus] = []

class TrainerBehaviorEvent(BehaviorEvent):
    trainer_name: str | None = None
    referral_date: str 
    notes: str | None = None