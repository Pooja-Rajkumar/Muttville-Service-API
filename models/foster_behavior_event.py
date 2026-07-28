from enum import Enum

from models.behavior_event import BehaviorEvent

from enum import Enum

from models.behavior_event import BehaviorEvent


class StairBehaviorType(str, Enum):
    COMFORTABLE = "My mutt is comfortable going up and down 1 or more flights of stairs"
    CAN_USE = "Stairs - and can use them!"
    FEW_STAIRS = "My mutt can handle a few stairs if necessary"
    CARRY_PREFERENCE = "My mutt prefers to be carried up and/or down stairs" 
    CARRY = "Stairs - and I carry my mutt!"
    UNKNOWN = "I don't know how my mutt handles stairs"
    NO_STAIRS = "No stairs!"



class PottyBehaviorType(str, Enum):
    WALKS = "On walks"
    YARD = "In the yard - I take them out"
    YARD_DOOR = "In the yard - dog door"
    PEE_PADS = "In the house on pee pads"
    MARKING = "In the house off pee pads (e.g. marking in the house)"
    NO_POTTY = "Hasn't pottied yet"


class SleepBehaviorType(str, Enum):
    BED = "In my bed"
    DOG_BED = "On a dog bed"
    FLOOR = "On the floor"


class EngagementBehaviorType(str, Enum):
    ACTIVE = "Actively engages"
    IGNORE = "Ignores them"
    AVOID = "Prefers to avoid"
    GUARDING = "Shows guarding behaviors"
    NOT_OBSERVED = "Not observed"


class EnjoymentBehaviorType(str, Enum):
    ENJOYS = "Enjoys"
    NEUTRAL = "Neutral"
    NERVOUS = "Nervous"
    NOT_OBSERVED = "Not observed"


class LeashBehaviorType(str, Enum):
    BARKS_AT_DOGS = "Barks at other dogs"
    BARKS_AT_HUMANS = "Barks at humans"
    BARKS_AT_MOVEMENT = (
        "Barks at bikes, skateboards, other unusual movements"
    )
    MEANDERS = "Likes to meander and smell all the things"
    WALKS_BRISKLY = "Likes to walk briskly"
    LONG_WALKS = "Would like to walk as long as they can!"
    WANTS_TO_STOP = (
        "Would like to stop walking and go back to the couch"
    )


class SoloMuttBehaviorType(str, Enum):
    SETTLED = "Hardly notice I'm gone"
    VOCAL = "Vocalize a little and then settle down"
    ANXIOUS = (
        "Vocalize for an extended time and/or shows other anxious behaviors"
    )
class FosterBehaviorEvent(BehaviorEvent):
    stairs_behavior: list[StairBehaviorType] | None = None
    potty_behavior: list[PottyBehaviorType] | None = None

    sleep_behavior: list[SleepBehaviorType] | None = None
    sleep_behavior_other_text: str | None = None

    # Social experiences at foster home
    dogs_foster_home: EngagementBehaviorType | None = None
    cats_foster_home: EngagementBehaviorType | None = None
    adults_foster_home: EngagementBehaviorType | None = None
    kids_12_under_foster_home: EngagementBehaviorType | None = None
    kids_13_over_foster_home: EngagementBehaviorType | None = None

    # Social experiences at someone else's home
    dogs_other_home: EngagementBehaviorType | None = None
    cats_other_home: EngagementBehaviorType | None = None
    adults_other_home: EngagementBehaviorType | None = None
    kids_12_under_other_home: EngagementBehaviorType | None = None
    kids_13_over_other_home: EngagementBehaviorType | None = None

    # Other experiences
    car_rides: EnjoymentBehaviorType | None = None
    public_transportation: EnjoymentBehaviorType | None = None
    carriers_strollers: EnjoymentBehaviorType | None = None
    mobility_devices: EnjoymentBehaviorType | None = None
    toys: EnjoymentBehaviorType | None = None

    # Handling experiences
    being_petted: EnjoymentBehaviorType | None = None

    leash_behavior: list[LeashBehaviorType] | None = None
    solo_mutt_behavior: SoloMuttBehaviorType | None = None