from datetime import date

from app.hotels.rooms.dao import RoomDAO
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date
):
    return await RoomDAO.get_rooms_for_hotel(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )


