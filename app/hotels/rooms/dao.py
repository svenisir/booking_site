from datetime import date

from sqlalchemy import select, func, ChunkedIteratorResult, case

from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker
from app.bookings.dao import BookingDAO


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def get_rooms_for_hotel(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        select  *, (date('2023-06-10')-date('2023-05-10'))*rooms.price,

        ) from rooms
        where hotel_id  = 5
        """
        async with async_session_maker() as session:
            booked_rooms = BookingDAO.get_rooms_left_query(
                date_from=date_from,
                date_to=date_to
            )

            get_rooms = select(
                cls.model.__table__.columns,
                ((date_to-date_from).days * Rooms.price).label("full_price"),
                case((Rooms.quantity - booked_rooms >= 0,
                      Rooms.quantity - booked_rooms),
                     else_=0).label("rooms_left")
            ).where(Rooms.hotel_id == hotel_id)

            rooms: ChunkedIteratorResult = await session.execute(get_rooms)
            return rooms.mappings().all()


