from datetime import datetime, timedelta
import re

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
        dog_names = re.split(r",|\s+and\s+", row["Pup Name"], flags=re.IGNORECASE)
        dog_names = [name.strip() for name in dog_names]  # Strip whitespace from
        location = row.get("Location", "HQ")
        if location == "Other":
            location = row.get("If location is other, please share details","Other",).strip()
       
        for dog_name in dog_names:
            events.append(
                BehaviorEvent(
                    timestamp=timestamp,
                    event_id= clean_string(timestamp) + "-" + dog_name,
                    dog_name=dog_name,
                    source=EventSource.SLACK_BEHAVIOR_UPDATES,
                summary=notes,
                inputted_by=clean_string(row.get("Submitted By")),
                location=location,
            )
        )

    return events