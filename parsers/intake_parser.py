from datetime import datetime

from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.helper import clean_string
from models.behavior_event import BehaviorEvent, EventSource


def parse_intake_info(rows: list[dict]) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        intake_notes = row.get("Intake Behavior Notes", "").strip()
        foster_response = row.get("Foster Response", "").strip()

        text = intake_notes
        details = {}
        if foster_response:
            text += " " + foster_response
            details["foster_response"] = foster_response

        events.append(
            BehaviorEvent(
                occurred_at=datetime.strptime(
                    row["Date - Intake"],
                    "%m/%d/%y",
                ),
                inputted_by=clean_string(row.get("Foster Name")),
                dog_name=clean_string(row.get("Dog Name")),
                source=EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
                concern=[classify_behavior_concern(text)],
                summary=intake_notes or "Intake behavior information recorded",
                details= details or None,
                raw_data=row,
            )
        )

    return events
