from unittest.mock import patch

from channels.behavior_modification import get_trainer_response
from channels.foster_questionnaire_responses import (
    get_foster_notes_questionaire_info_reviewer_expanded,
)
from channels.intake import get_intake_info
from channels.slack import get_slack_info
from channels.google_sheet_channel import (
    get_google_sheet_records,
    GoogleSheetSource,
)

from helpers.constants import (
    GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE,
    FOSTER_QUESTIONNAIRE_WORKSHEET_ID,
    FOSTER_QUESTIONNAIRE_COLUMN_NAME,
    GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET,
    TRAINER_WORKSHEET_ID,
    TRAINER_COLUMN_NAME,
    GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
    INTAKE_WORKSHEET_NAME,
    INTAKE_COLUMN_NAME,
    GOOGLE_SHEET_KEY_SLACK,
    SLACK_WORKSHEET_NAME,
    SLACK_COLUMN_NAME,
    ADOPTED,
)


def test_foster_questionnaire():
    records = [
        {FOSTER_QUESTIONNAIRE_COLUMN_NAME: "Foam", "Notes": "Calm"},
        {FOSTER_QUESTIONNAIRE_COLUMN_NAME: "Othello", "Notes": "Playful"},
        {FOSTER_QUESTIONNAIRE_COLUMN_NAME: "Foam", "Notes": "Restless"},
    ]

    with (
        patch(
            "channels.foster_questionnaire_responses.retrieve_google_sheet_records_by_id",
            return_value=records,
        ),
        patch(
            "channels.google_sheet_channel.retrieve_google_sheet_records_by_id",
            return_value=records,
        ),
    ):
        original_result = get_foster_notes_questionaire_info_reviewer_expanded("Foam")

        metadata = GoogleSheetSource(
            name="Foster Questionnaire",
            sheet_key=GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE,
            worksheet_name=None,
            worksheet_id=FOSTER_QUESTIONNAIRE_WORKSHEET_ID,
            desired_column_name=FOSTER_QUESTIONNAIRE_COLUMN_NAME,
        )

        new_result = get_google_sheet_records(
            metadata, "Foam", search_by_id=True
        )

    expected = [records[0], records[2]]

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result


def test_trainer():
    records = [
        {TRAINER_COLUMN_NAME: "Foam", "Trainer": "Alice"},
        {TRAINER_COLUMN_NAME: "Othello", "Trainer": "Bob"},
        {TRAINER_COLUMN_NAME: "Foam", "Trainer": "Charlie"},
    ]

    with (
        patch(
            "channels.behavior_modification.retrieve_google_sheet_records_by_id",
            return_value=records,
        ),
        patch(
            "channels.google_sheet_channel.retrieve_google_sheet_records_by_id",
            return_value=records,
        ),
    ):
        original_result = get_trainer_response("Foam")

        metadata = GoogleSheetSource(
            name="Trainer",
            sheet_key=GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET,
            worksheet_name=None,
            worksheet_id=TRAINER_WORKSHEET_ID,
            desired_column_name=TRAINER_COLUMN_NAME,
        )

        new_result = get_google_sheet_records(
            metadata, "Foam", search_by_id=True
        )

    expected = [records[0], records[2]]

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result


def test_slack():
    records = [
        {SLACK_COLUMN_NAME: "Foam", "Update": "Barked"},
        {SLACK_COLUMN_NAME: "Othello", "Update": "Played"},
        {SLACK_COLUMN_NAME: "Foam", "Update": "Settled"},
    ]

    with (
        patch(
            "channels.slack.retrieve_google_sheet_records_by_name",
            return_value=records,
        ),
        patch(
            "channels.google_sheet_channel.retrieve_google_sheet_records_by_name",
            return_value=records,
        ),
    ):
        original_result = get_slack_info("Foam")

        metadata = GoogleSheetSource(
            name="Slack Behavior Updates",
            sheet_key=GOOGLE_SHEET_KEY_SLACK,
            worksheet_name=SLACK_WORKSHEET_NAME,
            desired_column_name=SLACK_COLUMN_NAME,
        )

        new_result = get_google_sheet_records(metadata, "Foam")

    expected = [records[0], records[2]]

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result