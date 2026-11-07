from auth.google_sheet_connector import retrieve_google_sheet_records_by_id
from channels.google_sheet_channel import get_google_sheet_records
from channels.intake import get_intake_info
from database.database import save_behavior_events
from helpers.constants import GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE
from models.behavior_event import EventSource
from models.channel_model import GoogleSheetSource, Shelter
from parsers.behavior_modification_parser import parse_medication_info, parse_trainer_info
from parsers.foster_questionnaire_parser import parse_foster_questionnaire
from parsers.intake_parser import parse_intake_info
from parsers.slack_parser import parse_slack_behavior_updates
from config import muttville_config

# def backfill_medications(events: list[BehaviorEvent]):
#     sheet_data = retrieve_google_sheet_records_by_name(GOOGLE_SHEET_KEY_MEDICATIONS, MEDICATIONS_WORKSHEET_NAME)
#     events = parse_medication_info(sheet_data)
#     save_behavior_events(events)

# def backfill_trainer_responses(shelter_config: Shelter):
#     sheet_data = retrieve_google_sheet_records_by_id(GOOGLE_SHEET_KEY_MUTT_CHEAT_SHEET, 1665262541)
#     events = parse_trainer_info(sheet_data)
#     save_behavior_events(events)

# def backfill_foster_questionnaire():
#     sheet_data = retrieve_google_sheet_records_by_id(GOOGLE_SHEET_KEY_FOSTER_QUESTIONAIRE, 637846814)
#     events = parse_foster_questionnaire(sheet_data)
#     save_behavior_events(events)

# INTAKE IS WRONG THIS WHOLE TIME????
def backfill_intake(): 
    pass

# def backfill_slack(shelter_config: Shelter):
#     sheet_data = retrieve_google_sheet_records_by_name(GOOGLE_SHEET_KEY_SLACK, "Form Responses")
#     events = parse_slack_behavior_updates(sheet_data)
#     save_behavior_events(events)

def choose_parser(source_name: str):
    print("source_name ==", source_name)
    if source_name == EventSource.GS_FOSTER_QUESTIONNAIRE:
        return parse_foster_questionnaire
    elif source_name == EventSource.GS_MEDICATIONS:
        return parse_medication_info
    elif source_name == EventSource.GS_MUTT_CHEAT_SHEET:
        return parse_trainer_info
    elif source_name == EventSource.SLACK_BEHAVIOR_UPDATES:
        return parse_slack_behavior_updates
    else:
        raise ValueError(f"No parser defined for source: {source_name}")

def backfill_channel(source: GoogleSheetSource):
    records = get_google_sheet_records(source) 
    parser = choose_parser(source.name)
    print("parser ==", parser)
    events = parser(records)
    save_behavior_events(events)

def backfill(shelter_config: Shelter):
    print("shelter confiig ==", shelter_config)
    if shelter_config.name == "Muttville Senior Dog Rescue":
        for channel in shelter_config.channels: 
            for source in channel.sources:
                #backfill_channel(source)
                if source.name == EventSource.GS_BEHAVIORAL_OUTREACH_FOSTER:
                    backfill_intake() # specialized backfill for muttville
                else:
                    backfill_channel(source)
    else:
        print(f"Backfill not implemented for shelter: {shelter_config.name}")

def backfill_all():
    backfill(muttville_config)
    # backfill_medications()
    # backfill_trainer_responses()
    # backfill_foster_questionnaire()
    # backfill_intake()
    # backfill_slack()
