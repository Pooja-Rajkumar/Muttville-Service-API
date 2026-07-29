from models.behavior_event import BehaviorEvent

class MedicationBehaviorEvent(BehaviorEvent):
    medication: str | None = None
    location: str | None = None

class TrainerBehaviorEvent(BehaviorEvent):
    trainer_name: str | None = None
    referral_date: str | None = None
    notes: str | None = None