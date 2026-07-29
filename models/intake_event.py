
from models.behavior_event import BehaviorEvent

class IntakeEvent(BehaviorEvent):
    foster_response: str | None = None