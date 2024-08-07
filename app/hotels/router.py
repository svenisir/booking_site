from datetime import date, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exeptions import (
    DateToGradeThenDateFromException,
    HotelIsNotExistException,
    InvalidBookingTimeException,
)
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotelsLocation

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels(
        location: str,
        date_from: date = Query(..., description=f"Например: {date.today()}"),
        date_to: date = Query(..., description=f"Например: {date.today() + timedelta(days=14)}")
) -> list[SHotelsLocation]:
    if date_from >= date_to:
        raise DateToGradeThenDateFromException
    elif date_to - date_from > timedelta(days=30):
        raise InvalidBookingTimeException

    hotels = await HotelDAO.get_hotels(
        location=location,
        date_from=date_from,
        date_to=date_to
    )
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotels_by_id(hotel_id: int) -> SHotels:
    hotel = await HotelDAO.find_by_id(model_id=hotel_id)
    if not hotel:
        raise HotelIsNotExistException
    return hotel
