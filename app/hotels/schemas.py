from pydantic import BaseModel, ConfigDict, Field, JsonValue


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: JsonValue
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SHotelsLocation(BaseModel):
    id: int
    name: str
    location: str
    services: JsonValue
    rooms_quantity: int
    image_id: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)

