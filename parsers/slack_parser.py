from datetime import datetime, timedelta

from helpers.behavior_concern_classifier import classify_behavior_concern
from helpers.helper import clean_string
from models.behavior_event import BehaviorEvent, EventSource

def parse_slack_behavior_updates(rows: list[dict]) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        timestamp = datetime.strptime(
            row["Timestamp"],
            "%b %d, %Y, %I:%M:%S %p",
        ) - timedelta(hours=7)

        notes = row.get("Pup Notes", "").strip()
        dog_name = row["Pup Name"]
        events.append(
            BehaviorEvent(
                timestamp=timestamp,
                event_id= clean_string(timestamp) + "-" + dog_name,
                dog_name=dog_name,
                source=EventSource.SLACK_BEHAVIOR_UPDATES,
                concerns=[classify_behavior_concern(notes)],
                summary=notes,
                inputted_by=clean_string(row.get("Submitted By")),
            )
        )

    return events