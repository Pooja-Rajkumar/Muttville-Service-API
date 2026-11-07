
from unittest.mock import patch

from channels.intake import (
    get_intake_info,
    get_google_sheet_intake_records,
)
from models.channel_model import GoogleSheetSource
from helpers.constants import (
    ADOPTED,
    GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
    INTAKE_WORKSHEET_NAME,
    INTAKE_COLUMN_NAME,
)


def test_intake():
    records = [
        {INTAKE_COLUMN_NAME: "Foam", "SL Status": "In Foster"},
        {INTAKE_COLUMN_NAME: "Foam", "SL Status": ADOPTED},
        {INTAKE_COLUMN_NAME: "Othello", "SL Status": "In Foster"},
        {INTAKE_COLUMN_NAME: "Foam", "SL Status": "At HQ"},
    ]

    metadata = GoogleSheetSource(
        name="Intake",
        sheet_key=GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
        worksheet_name=INTAKE_WORKSHEET_NAME,
        desired_column_name=INTAKE_COLUMN_NAME,
    )

    with patch(
        "channels.intake.retrieve_google_sheet_records_by_name",
        return_value=records,
    ) as mock_retrieve:
        original_result = get_intake_info("Foam")
        new_result = get_google_sheet_intake_records(metadata, "Foam")

    expected = [records[0], records[3]]

    assert original_result == expected
    assert new_result == expected
    assert new_result == original_result

    # Verify both functions retrieved from the same worksheet.
    assert mock_retrieve.call_count == 2
    mock_retrieve.assert_called_with(
        GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
        INTAKE_WORKSHEET_NAME,
    )
