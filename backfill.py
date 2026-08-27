from auth.google_sheet_connector import get_google_sheet
from database.database import save_behavior_event
from helpers.constants import GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, GOOGLE_SHEET_KEY_MEDICATIONS, GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, GOOGLE_SHEET_KEY_SLACK
from parsers.behavior_modification_parser import parse_medication_info, parse_trainer_info
from parsers.foster_questionnaire_parser import parse_foster_questionnaire
from parsers.slack_parser import parse_slack_behavior_updates


def backfill_medications():
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MEDICATIONS)
    sheet_data = sheet.worksheet("Form Responses 1").get_all_records()
    events = parse_medication_info(sheet_data)
    for event in events:
        save_behavior_event(event)

def backfill_trainer_responses():
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET)
    tab_id = 1665262541
    sheet_data = sheet.get_worksheet_by_id(tab_id).get_all_records()
    events = parse_trainer_info(sheet_data)
    for event in events:
        save_behavior_event(event)

def backfill_foster_questionnaire():
    # aggregate foster notes questionaire info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE)
    target_sheet_id = 637846814 # Reviewer View (Expanded) tab
    worksheet = sheet.get_worksheet_by_id(target_sheet_id)
    sheet_data = worksheet.get_all_records()
    events = parse_foster_questionnaire(sheet_data)
    for event in events:
        save_behavior_event(event)

def backfill_intake():
    # aggregate intake info from google sheet once workflow is up 
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE)
    target_sheet_id = 637846814 # Reviewer View (Expanded) tab
    worksheet = sheet.get_worksheet_by_id(target_sheet_id)
    sheet_data = worksheet.get_all_records()
    events = parse_foster_questionnaire(sheet_data)
    for event in events:
        save_behavior_event(event)

def backfill_slack():
    sheet = get_google_sheet(GOOGLE_SHEET_KEY_SLACK)
    sheet_data = sheet.worksheet("Form Responses").get_all_records()
    events = parse_slack_behavior_updates(sheet_data)
    for event in events:
        save_behavior_event(event)

def backfill_all():
    backfill_medications()
    backfill_trainer_responses()
    backfill_foster_questionnaire()
    backfill_intake()
    backfill_slack()
