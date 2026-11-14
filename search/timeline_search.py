import re

from models.behavior_event import BehaviorEvent
from rapidfuzz import fuzz, process


def normalize_dog_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())

def group_dog_names(events: list[BehaviorEvent]) -> dict[str, set[str]]:
    groups = {}
    for event in events:
        normalized = normalize_dog_name(event.dog_name)
        if normalized not in groups:
            groups[normalized] = set()
        groups[normalized].add(event.dog_name)

    for normalized in groups:
        groups[normalized] = sorted(groups[normalized])

    return groups


def find_matching_dogs(
    search_term: str,
    dog_groups: dict[str, set[str]],
) -> dict[str, set[str]]:

    search_term = normalize_dog_name(search_term)
    matches = {}

    if not search_term:
        return matches

    for normalized_name, original_names in dog_groups.items():
        if search_term in normalized_name:
            matches[normalized_name] = original_names

    return matches


def find_fuzzy_matches(
    search_term: str,
    dog_groups: dict[str, set[str]],
) -> dict[str, set[str]]:
    search_term = normalize_dog_name(search_term)

    results = process.extract(
        search_term,
        list(dog_groups.keys()),
        scorer=fuzz.partial_ratio,
        score_cutoff=80,
        limit=3,
    )

    matches = {}

    for normalized_name, _, _ in results:
        matches[normalized_name] = dog_groups[normalized_name]

    return matches