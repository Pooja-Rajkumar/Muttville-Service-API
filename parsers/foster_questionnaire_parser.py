from datetime import datetime
from enum import Enum

from helpers.behavior_concern_classifier import classify_foster_behavior_concerns
from helpers.helper import clean_string
from models.behavior_event import BehaviorEvent, EventSource
from models.foster_behavior_event import (
    EngagementBehaviorType,
    EnjoymentBehaviorType,
    FosterBehaviorEvent,
    LeashBehaviorType,
    PottyBehaviorType,
    SleepBehaviorType,
    SoloMuttBehaviorType,
    StairBehaviorType,
)
from parsers.behavior_modification_parser import classify_behavior_concern


def parse_foster_questionnaire(
    rows: list[dict],
) -> list[BehaviorEvent]:
    events = []

    for row in rows:
        summary = row.get("Favorite Things", "").strip()

        stairs_behavior = parse_checkbox_behavior(
            row.get("Stairs"),
            StairBehaviorType,
        )

        potty_behavior = parse_checkbox_behavior(
            row.get("Potty"),
            PottyBehaviorType,
        )

        sleep_behavior, sleep_behavior_other_text = parse_sleep_behavior(
            row.get("Sleep")
        )

        leash_behavior = parse_checkbox_behavior(
            row.get("Leash walking"),
            LeashBehaviorType,
        )

        solo_mutt_behavior = parse_single_behavior(
            row.get("Alone time"),
            SoloMuttBehaviorType,
        )

        behavior_details = {
            "stairs": row.get("Stairs"),
            "potty": row.get("Potty"),
            "sleep": row.get("Sleep"),
            "dogs_foster_home": row.get("Dogs (Foster Home)"),
            "cats_foster_home": row.get("Cats (Foster Home)"),
            "adults_foster_home": row.get("Adults (Foster Home)"),
            "kids_12_under_foster_home": row.get(
                "Kids 12 & under (Foster Home)"
            ),
            "kids_13_over_foster_home": row.get(
                "Kids 13 & over (Foster Home)"
            ),
            "dogs_other_home": row.get("Dogs (Other Home)"),
            "cats_other_home": row.get("Cats (Other Home)"),
            "adults_other_home": row.get("Adults (Other Home)"),
            "kids_12_under_other_home": row.get(
                "Kids 12 & under (Other Home)"
            ),
            "kids_13_over_other_home": row.get(
                "Kids 13 & over (Other Home)"
            ),
            "car_rides": row.get("Car rides"),
            "public_transportation": row.get("Public transportation"),
            "carriers_strollers": row.get("Carriers/strollers"),
            "mobility_devices": row.get("Canes/walkers/wheelchairs"),
            "toys": row.get("Toys"),
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
                "for the Muttville team to know about your mutt?"
            ),
        }
        dogs_foster_home = parse_single_behavior(
            row.get("Dogs (Foster Home)"),
            EngagementBehaviorType,
        )

        cats_foster_home = parse_single_behavior(
            row.get("Cats (Foster Home)"),
            EngagementBehaviorType,
        )

        being_petted = parse_single_behavior(
            row.get("Being petted"),
            EnjoymentBehaviorType,
        )

        getting_picked_up = parse_single_behavior(
            row.get("Getting picked up"),
            EnjoymentBehaviorType,
        )

        baths = parse_single_behavior(
            row.get("Baths"),
            EnjoymentBehaviorType,
        )
        dogs_other_home = parse_single_behavior(
            row.get("Dogs (Other Home)"),
            EngagementBehaviorType,
        )
        cats_other_home=parse_single_behavior(
            row.get("Cats (Other Home)"),
            EngagementBehaviorType,
        )

        concerns = classify_foster_behavior_concerns(
            dogs_foster_home=dogs_foster_home,
            cats_foster_home=cats_foster_home,
            dogs_other_home=dogs_other_home,
            cats_other_home=cats_other_home,
            being_petted=being_petted,
            getting_picked_up=getting_picked_up,
            baths=baths,
            leash_behavior=leash_behavior,
            solo_mutt_behavior=solo_mutt_behavior,
)

        events.append(
            FosterBehaviorEvent(
                occurred_at=datetime.strptime(
                    row["Submission Date/Time"],
                    "%m/%d/%Y %H:%M:%S",
                ),
                inputted_by=clean_string(row.get("Your Name")),
                dog_name=clean_string(row.get("Mutt's Name")),
                source=EventSource.GS_FOSTER_QUESTIONNAIRE,
                summary=summary or "Foster questionnaire submitted",
                details=behavior_details,
                concerns=concerns,
                stairs_behavior=stairs_behavior,
                potty_behavior=potty_behavior,

                sleep_behavior=sleep_behavior,
                sleep_behavior_other_text=sleep_behavior_other_text,

                # Social behavior at foster home
                dogs_foster_home=dogs_foster_home,
                cats_foster_home=cats_foster_home,
                adults_foster_home=parse_single_behavior(
                    row.get("Adults (Foster Home)"),
                    EngagementBehaviorType,
                ),
                kids_12_under_foster_home=parse_single_behavior(
                    row.get("Kids 12 & under (Foster Home)"),
                    EngagementBehaviorType,
                ),
                kids_13_over_foster_home=parse_single_behavior(
                    row.get("Kids 13 & over (Foster Home)"),
                    EngagementBehaviorType,
                ),

                # Social behavior at someone else's home
                dogs_other_home=dogs_other_home,
                cats_other_home=cats_other_home,
                adults_other_home=parse_single_behavior(
                    row.get("Adults (Other Home)"),
                    EngagementBehaviorType,
                ),
                kids_12_under_other_home=parse_single_behavior(
                    row.get("Kids 12 & under (Other Home)"),
                    EngagementBehaviorType,
                ),
                kids_13_over_other_home=parse_single_behavior(
                    row.get("Kids 13 & over (Other Home)"),
                    EngagementBehaviorType,
                ),

                # Other experiences
                car_rides=parse_single_behavior(
                    row.get("Car rides"),
                    EnjoymentBehaviorType,
                ),
                public_transportation=parse_single_behavior(
                    row.get("Public transportation"),
                    EnjoymentBehaviorType,
                ),
                carriers_strollers=parse_single_behavior(
                    row.get("Carriers/strollers"),
                    EnjoymentBehaviorType,
                ),
                mobility_devices=parse_single_behavior(
                    row.get("Canes/walkers/wheelchairs"),
                    EnjoymentBehaviorType,
                ),
                toys=parse_single_behavior(
                    row.get("Toys"),
                    EnjoymentBehaviorType,
                ),

                # Handling experiences
                being_petted=being_petted,
                getting_picked_up=getting_picked_up,
                baths=baths,
                leash_behavior=leash_behavior,
                solo_mutt_behavior=solo_mutt_behavior,

                raw_data=row,
            )
        )

    return events


def parse_checkbox_behavior(
    value: str | None,
    enum_class: type[Enum],
):
    if not value:
        return []

    selected_behaviors = []

    for behavior in enum_class:
        if behavior.value in value:
            selected_behaviors.append(behavior)

    return selected_behaviors

def parse_single_behavior(
    value: str | None,
    enum_class: type[Enum],
):
    if not value:
        return None

    return enum_class(value.strip())


def parse_sleep_behavior(
    value: str | None,
) -> tuple[list[SleepBehaviorType], str | None]:
    if not value:
        return [], None

    known_behaviors = {
        behavior.value
        for behavior in SleepBehaviorType
    }

    selections = [
        selection.strip()
        for selection in value.split(",")
        if selection.strip()
    ]

    sleep_behavior = []
    other_text = None

    for selection in selections:
        if selection in known_behaviors:
            sleep_behavior.append(
                SleepBehaviorType(selection)
            )
        else:
            other_text = selection

    return sleep_behavior, other_text