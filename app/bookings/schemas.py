from typing import Union
from datetime import date

from pydantic import BaseModel, ConfigDict, JsonValue, StrictStr


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class SBookingForUser(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: Union[str, None]
    services: JsonValue

    model_config = ConfigDict(from_attributes=True)
