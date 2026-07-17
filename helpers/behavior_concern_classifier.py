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