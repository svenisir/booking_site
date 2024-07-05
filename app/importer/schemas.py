from datetime import date
from pydantic import BaseModel, JsonValue


class SBookingCSV(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date


class SHotelsCSV(BaseModel):
    name: str
    location: str
    services: JsonValue
    rooms_quantity: int
    image_id: int


class SRoomCSV(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: JsonValue
    quantity: int
    image_id: int
