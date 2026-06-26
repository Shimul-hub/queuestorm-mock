from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.enums import Channel, Locale


class SortTicketRequest(BaseModel):
    ticket_id: str = Field(..., min_length=1)
    channel: Channel | None = None
    locale: Locale | None = None
    message: str = Field(..., min_length=1, max_length=5000)

    @field_validator("channel", mode="before")
    @classmethod
    def coerce_channel(cls, value: Any) -> Channel | None:
        if value is None or value == "":
            return None
        try:
            return Channel(value)
        except ValueError:
            return None

    @field_validator("locale", mode="before")
    @classmethod
    def coerce_locale(cls, value: Any) -> Locale | None:
        if value is None or value == "":
            return None
        try:
            return Locale(value)
        except ValueError:
            return None
