from sqlalchemy import select, insert, func, and_, or_, ChunkedIteratorResult

from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker

from datetime import date


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = cls.get_rooms_left_query(
                date_from=date_from,
                date_to=date_to
            )

            get_rooms_left = select(
                (Rooms.quantity - booked_rooms).label("rooms_left")
            ).select_from(Rooms).where(Rooms.id == room_id)

            rooms_left: ChunkedIteratorResult = await session.execute(get_rooms_left)
            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price: ChunkedIteratorResult = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings.__table__.columns)

                new_booking: ChunkedIteratorResult = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one_or_none()
            else:
                return None

    @classmethod
    async def find_all_by_user_id(cls, user_id):
        async with async_session_maker() as session:
            get_bookings = select(
                Bookings.id, Bookings.room_id, Bookings.user_id,
                # Bookings.date_from, Bookings.date_to, Bookings.price,
                # Bookings.total_cost, Bookings.total_days, Rooms.image_id,
                # Rooms.name, Rooms.description, Rooms.services
            ).select_from(Bookings).join(
                Rooms, Bookings.room_id == Rooms.id, isouter=True
            ).where(Bookings.user_id == user_id)
            bookings: ChunkedIteratorResult = await session.execute(get_bookings)
            return bookings.mappings().all()

    @staticmethod
    def get_rooms_left_query(
            date_from: date,
            date_to: date,
            **filter_by
    ):
        """
        select * from bookings
        where room_id = 1 and
            ((date_from >= '2033-05-15' and date_to <= '2033-06-20') or
            (date_from <= '2033-05-15' and date_to >= '2033-05-15') or
            (date_from <= '2033-06-20' and date_to >= '2033-06-20'))

        """
        booked_rooms = select(func.count(Bookings.id)).where(
            and_(
                Bookings.room_id == Rooms.id,
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_to <= date_to
                    ),
                    or_(
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to >= date_from
                        ),
                        and_(
                            Bookings.date_from <= date_to,
                            Bookings.date_to >= date_to
                        ),
                    )
                )
            )
        ).scalar_subquery()

        return booked_rooms
