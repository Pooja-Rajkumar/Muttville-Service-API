from models.behavior_event import BehaviorConcern


## TODO: Need to replace this with something smarter, maybe a ML model or something. For now, just using simple keyword matching to classify behavior concerns.
def classify_behavior_concern(
    summary: str,
    notes: str | None = None,
) -> BehaviorConcern:
    text = f"{summary} {notes or ''}".lower()

    if any(
        phrase in text
        for phrase in (
            "left alone",
            "separation",
            "when separated",
            "scratching at doors",
            "inability to settle",
        )
    ):
        return BehaviorConcern.SEPARATION_DISTRESS

    if any(
        phrase in text
        for phrase in (
            "on leash",
            "leash reactive",
            "lunging",
            "barking at dogs",
            "meeting new dogs",
        )
    ):
        return BehaviorConcern.LEASH_REACTIVITY

    if any(
        phrase in text
        for phrase in (
            "handling",
            "picked up",
            "eye meds",
            "nippy",
            "bit",
            "bite",
            "grooming",
            "nail trim",
        )
    ):
        return BehaviorConcern.HANDLING_SENSITIVITY

    if any(
        phrase in text
        for phrase in (
            "resource guarding",
            "guarding food",
            "guarding toy",
            "guarding bed",
        )
    ):
        return BehaviorConcern.RESOURCE_GUARDING

    if any(
        phrase in text
        for phrase in (
            "potty",
            "pee",
            "poop",
            "accident",
            "house trained",
            "house-training",
        )
    ):
        return BehaviorConcern.POTTY_TRAINING

    if any(
        phrase in text
        for phrase in (
            "resident dog",
            "resident cat",
            "new dog",
            "new dogs",
            "introduction",
            "introduced to",
        )
    ):
        return BehaviorConcern.INTROS_TO_RESIDENT_PET

    return BehaviorConcern.OTHER



from models.behavior_event import BehaviorConcern
from models.foster_behavior_event import (
    EngagementBehaviorType,
    EnjoymentBehaviorType,
    LeashBehaviorType,
    SoloMuttBehaviorType,
)


def classify_foster_behavior_concerns(
    dogs_foster_home: EngagementBehaviorType | None = None,
    cats_foster_home: EngagementBehaviorType | None = None,
    dogs_other_home: EngagementBehaviorType | None = None,
    cats_other_home: EngagementBehaviorType | None = None,
    being_petted: EnjoymentBehaviorType | None = None,
    getting_picked_up: EnjoymentBehaviorType | None = None,
    baths: EnjoymentBehaviorType | None = None,
    leash_behavior: list[LeashBehaviorType] | None = None,
    solo_mutt_behavior: SoloMuttBehaviorType | None = None,
) -> list[BehaviorConcern]:

    concerns = []

    # Separation distress
    if solo_mutt_behavior == SoloMuttBehaviorType.ANXIOUS:
        concerns.append(BehaviorConcern.SEPARATION_DISTRESS)

    # Leash reactivity
    if leash_behavior:
        reactive_leash_behaviors = {
            LeashBehaviorType.BARKS_AT_DOGS,
            LeashBehaviorType.BARKS_AT_HUMANS,
            LeashBehaviorType.BARKS_AT_MOVEMENT,
        }

        for behavior in leash_behavior:
            if behavior in reactive_leash_behaviors:
                concerns.append(BehaviorConcern.LEASH_REACTIVITY)
                break

    # Handling sensitivity
    handling_behaviors = [
        being_petted,
        getting_picked_up,
        baths,
    ]

    for behavior in handling_behaviors:
        if behavior == EnjoymentBehaviorType.NERVOUS:
            concerns.append(BehaviorConcern.HANDLING_SENSITIVITY)
            break

    # Resource guarding
    social_behaviors = [
        dogs_foster_home,
        cats_foster_home,
        dogs_other_home,
        cats_other_home,
    ]

    for behavior in social_behaviors:
        if behavior == EngagementBehaviorType.GUARDING:
            concerns.append(BehaviorConcern.RESOURCE_GUARDING)
            break

    # Resident pet introductions
    pet_social_behaviors = [
        dogs_foster_home,
        cats_foster_home,
        dogs_other_home,
        cats_other_home,
    ]

    concerning_pet_responses = {
        EngagementBehaviorType.AVOID,
        EngagementBehaviorType.GUARDING,
    }

    for behavior in pet_social_behaviors:
        if behavior in concerning_pet_responses:
            concerns.append(BehaviorConcern.INTROS_TO_RESIDENT_PET)
            break

    if not concerns:
        concerns.append(BehaviorConcern.OTHER)

    return concerns