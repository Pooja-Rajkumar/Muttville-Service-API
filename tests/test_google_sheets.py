
from unittest.mock import MagicMock

import pytest
from auth import google_sheet_connector
import main
import helpers.constants as constants
from auth.google_sheet_connector import (
    retrieve_google_records_by_name,
    retrieve_google_records_by_id,
    find_matching_records,
)


MEDICATION_RECORDS = [
    {"Dog's name": "Foam", "Medication": "Trazodone"},
    {"Dog's name": "Othello", "Medication": "Gabapentin"},
    {"Dog's name": "Foam", "Medication": "Fluoxetine"},
]

TRAINER_RECORDS = [
    {"Dog Name": "Foam", "Trainer": "Alice"},
    {"Dog Name": "Othello", "Trainer": "Bob"},
    {"Dog Name": "Foam", "Trainer": "Charlie"},
]


@pytest.fixture
def mock_google_sheets(monkeypatch):
    client = MagicMock()
    sheet = MagicMock()

    client.open_by_key.return_value = sheet

    sheet.worksheet.return_value.get_all_records.return_value = (
        MEDICATION_RECORDS
    )

    sheet.get_worksheet_by_id.return_value.get_all_records.return_value = (
        TRAINER_RECORDS
    )

    monkeypatch.setattr(
        google_sheet_connector,
        "get_client",
        lambda: client,
    )

    return sheet


@pytest.mark.parametrize(
    "dog_name, expected",
    [
        (
            "Foam",
            [
                {"Dog's name": "Foam", "Medication": "Trazodone"},
                {"Dog's name": "Foam", "Medication": "Fluoxetine"},
            ],
        ),
        (
            "foam",
            [
                {"Dog's name": "Foam", "Medication": "Trazodone"},
                {"Dog's name": "Foam", "Medication": "Fluoxetine"},
            ],
        ),
        (
            "Othello",
            [{"Dog's name": "Othello", "Medication": "Gabapentin"}],
        ),
        ("Unknown Dog", []),
    ],
)
def test_medications_matches_original(
    mock_google_sheets, dog_name, expected
):
    original_result = main.get_medications_info(dog_name)

    records = retrieve_google_records_by_name(
        constants.GOOGLE_SHEET_KEY_MEDICATIONS,
        "Form Responses 1",
    )

    new_result = find_matching_records(
        records,
        "Dog's name",
        dog_name,
    )

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result

    mock_google_sheets.worksheet.assert_called_with("Form Responses 1")


@pytest.mark.parametrize(
    "dog_name, expected",
    [
        (
            "Foam",
            [
                {"Dog Name": "Foam", "Trainer": "Alice"},
                {"Dog Name": "Foam", "Trainer": "Charlie"},
            ],
        ),
        (
            "OTHELLO",
            [{"Dog Name": "Othello", "Trainer": "Bob"}],
        ),
        ("Unknown Dog", []),
    ],
)
def test_trainer_matches_original(
    mock_google_sheets, dog_name, expected
):
    original_result = main.get_trainer_response(dog_name)

    records = retrieve_google_records_by_id(
        constants.GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET,
        1665262541,
    )

    new_result = find_matching_records(
        records,
        "Dog Name",
        dog_name,
    )

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result

    mock_google_sheets.get_worksheet_by_id.assert_called_with(
        1665262541
    )
