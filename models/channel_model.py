from enum import Enum
from typing import Literal
from pydantic import BaseModel, Field, model_validator

from models.behavior_event import EventSource

class ChannelType(str, Enum):
    GOOGLE_SHEET = "Google Sheet"
    SLACK = "Slack"

class Channel(BaseModel):
    name: ChannelType
    sources: list[GoogleSheetSource | SlackSource] = Field(default_factory=list)

class Source(BaseModel):
    name: EventSource
    channel_type: ChannelType

class GoogleSheetSource(Source):
    channel_type: Literal[ChannelType.GOOGLE_SHEET] = ChannelType.GOOGLE_SHEET
    sheet_key: str
    worksheet_name: str | None = None
    worksheet_id: int | None = None
    desired_column_name: str
    
    @model_validator(mode="after")
    def validate_worksheet(self):
        if (self.worksheet_name is None) == (self.worksheet_id is None):
            raise ValueError("Provide either worksheet_name or worksheet_id")
        return self

class SlackSource(Source):
    channel_type: Literal[ChannelType.SLACK] = ChannelType.SLACK
    slack_channel_id: str

class Shelter(BaseModel):
    name: str
    channels: list[Channel] = Field(default_factory=list)


