from datetime import datetime

from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.helper import clean_string
from models.behavior_event import BehaviorEvent, EventSource
from models.intake_event import IntakeEvent


def parse_intake_info(rows: list[dict]) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        intake_notes = row.get("Intake Behavior Notes", "").strip()
        foster_response = row.get("Foster Response", "").strip()
        events.append(
            IntakeEvent(
                timestamp=datetime.strptime(
                    row["Date - Intake"],
                    "%m/%d/%y",
                ),
                inputted_by=clean_string(row.get("Foster Name")),
                dog_name=clean_string(row.get("Dog Name")),
                source=EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
                concerns=[classify_behavior_concern(intake_notes)],
                summary=intake_notes or "Intake behavior information recorded",
                foster_response=foster_response or None,
                raw_data=row,
            )
        )

    return events
