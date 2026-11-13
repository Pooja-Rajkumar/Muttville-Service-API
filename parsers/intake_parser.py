from datetime import datetime

from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.constants import DOG_NAME
from helpers.helper import clean_string
from models.behavior_event import BehaviorEvent, EventSource
from models.intake_event import IntakeEvent


def parse_intake_info(rows: list[dict]) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        intake_notes = row.get("Intake Behavior Notes", "").strip()
        foster_response = row.get("Foster Response", "").strip()
        dates = row.get("Date - Intake", "").strip().split()
        if not dates:
            continue
        for date_intake in dates:
            events.append(
                IntakeEvent(
                    timestamp=datetime.strptime(
                        date_intake,
                        "%m/%d/%y",
                    ),
                    inputted_by="Intake Team",
                    event_id=clean_string(row.get(DOG_NAME)) + "-" + date_intake,
                    dog_name=clean_string(row.get(DOG_NAME)),
                    source=EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
                    summary=intake_notes or "Intake behavior information recorded",
                    foster_response=foster_response or None,
                    location="HQ",
                )
            )

    return events
