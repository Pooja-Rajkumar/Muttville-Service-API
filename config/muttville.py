
from models.channel_model import (
    Shelter,
    Channel,
    ChannelType,
    GoogleSheetSource,
)

from helpers.constants import (
    GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE,
    GOOGLE_SHEET_KEY_SLACK,
    GOOGLE_SHEET_KEY_MEDICATIONS,
    GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
    GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET,
    MEDICATIONS_WORKSHEET_NAME,
    TRAINER_WORKSHEET_ID,
    FOSTER_QUESTIONNAIRE_WORKSHEET_ID,
    INTAKE_WORKSHEET_NAME,
    SLACK_WORKSHEET_NAME,
    SLACK_COLUMN_NAME,
    MEDS_COLUMN_NAME,
    TRAINER_COLUMN_NAME,
    INTAKE_COLUMN_NAME,
    FOSTER_QUESTIONNAIRE_COLUMN_NAME,
)

from models.behavior_event import EventSource


muttville_config = Shelter(
    name="Muttville Senior Dog Rescue",
    email_alias="@muttville.org",
    channels=[
        Channel(
            name=ChannelType.GOOGLE_SHEET,
            sources=[
                GoogleSheetSource(
                    name=EventSource.GS_MEDICATIONS,
                    sheet_key=GOOGLE_SHEET_KEY_MEDICATIONS,
                    worksheet_name=MEDICATIONS_WORKSHEET_NAME,
                    desired_column_name=MEDS_COLUMN_NAME,
                ),
                GoogleSheetSource(
                    name=EventSource.GS_MUTT_CHEAT_SHEET,
                    sheet_key=GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET,
                    worksheet_id=TRAINER_WORKSHEET_ID,
                    desired_column_name=TRAINER_COLUMN_NAME,
                ),
                GoogleSheetSource(
                    name=EventSource.GS_FOSTER_QUESTIONNAIRE,
                    sheet_key=GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE,
                    worksheet_id=FOSTER_QUESTIONNAIRE_WORKSHEET_ID,
                    desired_column_name=FOSTER_QUESTIONNAIRE_COLUMN_NAME,
                ),
                GoogleSheetSource(
                    name=EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER,
                    sheet_key=GOOGLE_SHEET_KEY_BEHAVIORAL_OUTREACH_FOSTER,
                    worksheet_name=INTAKE_WORKSHEET_NAME,
                    desired_column_name=INTAKE_COLUMN_NAME,
                ),
                GoogleSheetSource(
                    name=EventSource.SLACK_BEHAVIOR_UPDATES,
                    sheet_key=GOOGLE_SHEET_KEY_SLACK,
                    worksheet_name=SLACK_WORKSHEET_NAME,
                    desired_column_name=SLACK_COLUMN_NAME,
                ),
            ],
        ),
    ],
)
