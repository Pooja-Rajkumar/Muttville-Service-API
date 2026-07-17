from datetime import datetime, timedelta

from helpers.behavior_concern_classifier import classify_behavior_concern
from models.behavior_event import BehaviorEvent, EventSource

def parse_slack_behavior_updates(rows: list[dict]) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        timestamp = datetime.strptime(
            row["Timestamp"],
            "%b %d, %Y, %I:%M:%S %p",
        ) - timedelta(hours=7)

        notes = row.get("Pup Notes", "").strip()

        events.append(
            BehaviorEvent(
                occurred_at=timestamp,
                dog_name=row["Pup Name"],
                source=EventSource.SLACK_BEHAVIOR_UPDATES,
                concern=[classify_behavior_concern(notes)],
                summary=notes,
                raw_data=row,
            )
        )

    return events