import asyncio
from datetime import date, timedelta

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.schemas import SHotels, SHotelsLocation
from app.hotels.dao import HotelDAO
from app.exeptions import HotelIsNotExistException

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
