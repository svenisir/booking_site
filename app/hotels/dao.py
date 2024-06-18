from datetime import date

from sqlalchemy import select, func, and_, ChunkedIteratorResult

from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.dao import BookingDAO
from app.database import async_session_maker


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_hotels(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        """
        with r_l as (
	        select  hotel_id, sum(rooms.quantity  - (
                select count(*) from bookings
                where room_id = rooms.id and
                    ((date_from >= '2023-05-10' and date_to <= '2023-06-10') or
                    (date_from <= '2023-05-10' and date_to >= '2023-05-10') or
                    (date_from <= '2023-06-10' and date_to >= '2023-06-10'))
            )) as rooms_left from rooms
	        group by rooms.hotel_id
        )

        select hotels.*, r_l.rooms_left
        from hotels join r_l on hotels.id = r_l.hotel_id
        where hotels.location like '%Алтай%' and r_l.rooms_left > 0
        :return:
        """
        async with async_session_maker() as session:
            booked_rooms = BookingDAO.get_rooms_left_query(
                date_from=date_from,
                date_to=date_to
            )

            get_rooms_left = select(
                Rooms.hotel_id, func.sum(Rooms.quantity - booked_rooms).label("rooms_left")
            ).select_from(Rooms).group_by(Rooms.hotel_id).cte("get_rooms_left")

            get_hotels = select(
                Hotels.__table__.columns, get_rooms_left.c.rooms_left
            ).select_from(Hotels).join(
                get_rooms_left, Hotels.id == get_rooms_left.c.hotel_id
            ).where(
                and_(
                    get_rooms_left.c.rooms_left > 0,
                    Hotels.location.ilike(f"%{location}%")
                )
            )

            hotels: ChunkedIteratorResult = await session.execute(get_hotels)
            return hotels.mappings().all()


