from auth.google_sheet_connector import retrieve_google_records_by_id, retrieve_google_records_by_name
from database.database import save_behavior_events
from helpers.constants import GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, GOOGLE_SHEET_KEY_SLACK, MEDICATIONS_WORKSHEET_NAME
from parsers.behavior_modification_parser import parse_medication_info, parse_trainer_info
from parsers.foster_questionnaire_parser import parse_foster_questionnaire
from parsers.slack_parser import parse_slack_behavior_updates


def backfill_medications():
    sheet_data = retrieve_google_records_by_name(GOOGLE_SHEET_KEY_MEDICATIONS, MEDICATIONS_WORKSHEET_NAME)
    events = parse_medication_info(sheet_data)
    save_behavior_events(events)


def backfill_trainer_responses():
    sheet_data = retrieve_google_records_by_id(GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, 1665262541)
    events = parse_trainer_info(sheet_data)
    save_behavior_events(events)

def backfill_foster_questionnaire():
    sheet_data = retrieve_google_records_by_id(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, 637846814)
    events = parse_foster_questionnaire(sheet_data)
    save_behavior_events(events)

def backfill_intake():
    sheet_data = retrieve_google_records_by_id(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, 637846814)
    events = parse_foster_questionnaire(sheet_data)
    save_behavior_events(events)

def backfill_slack():
    sheet_data = retrieve_google_records_by_name(GOOGLE_SHEET_KEY_SLACK, "Form Responses")
    events = parse_slack_behavior_updates(sheet_data)
    save_behavior_events(events)

def backfill_all():
    backfill_medications()
    backfill_trainer_responses()
    backfill_foster_questionnaire()
    backfill_intake()
    backfill_slack()
