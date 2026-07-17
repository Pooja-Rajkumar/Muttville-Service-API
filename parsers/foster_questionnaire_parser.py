from datetime import datetime

from models.behavior_event import BehaviorEvent, EventSource
from parsers.behavior_modification_parser import classify_behavior_concern


def parse_foster_questionnaire(
    rows: list[dict],
) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        summary = row.get("Favorite Things", "").strip()

        behavior_details = {
            "stairs": row.get("Stairs"),
            "potty": row.get("Potty"),
            "sleep": row.get("Sleep"),
            "dogs_in_foster_home": row.get("Dogs (Foster Home)"),
            "cats_in_foster_home": row.get("Cats (Foster Home)"),
            "adults_in_foster_home": row.get("Adults (Foster Home)"),
            "kids_12_under": row.get(
                "Kids 12 & under (Foster Home)"
            ),
            "car_rides": row.get("Car rides"),
            "being_petted": row.get("Being petted"),
            "getting_picked_up": row.get("Getting picked up"),
            "baths": row.get("Baths"),
            "leash_walking": row.get("Leash walking"),
            "alone_time": row.get("Alone time"),
            "additional_notes": row.get("Anything to add"),
            "transition_notes": row.get(
                "Is there anything that would be helpful for a "
                "potential adopter to know when your mutt "
                "transitions into a new home?"
            ),
            "team_notes": row.get(
                "Is there anything else we that would be helpful "
                "for the Muttville team to know about your mutt? "
            ),
        }

        text_to_classify = " ".join(
            str(value)
            for value in behavior_details.values()
            if value
        )

        events.append(
            BehaviorEvent(
                occurred_at=datetime.strptime(
                    row["Submission Date/Time"],
                    "%m/%d/%Y %H:%M:%S",
                ),
                dog_name=row["Mutt's Name"],
                source=EventSource.GS_FOSTER_QUESTIONNAIRE,
                concern=[classify_behavior_concern(
                    text_to_classify,
                    summary,
                )],
                summary=summary or "Foster questionnaire submitted",
                details=behavior_details,
                raw_data=row,
            )
        )

    return [
        event.model_dump(
            exclude_none=True,
            exclude={"raw_data"}
        )
        for event in events
    ]
