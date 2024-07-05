from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None


@pytest.mark.parametrize("user_id, room_id, date_from, date_to", [
    (1, 3, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
    (2, 3, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
    (1, 4, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
    (2, 4, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
    (1, 5, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
    (2, 5, datetime.strptime("2023-07-10", "%Y-%m-%d"),
     datetime.strptime("2023-07-24", "%Y-%m-%d")),
])
async def test_crud_booking(user_id, room_id, date_from, date_to):
    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    booking_id = new_booking.id
    booking = await BookingDAO.find_by_id(model_id=booking_id)
    assert booking.id == booking_id

    await BookingDAO.delete_by_id(model_id=booking_id)
    booking = await BookingDAO.find_by_id(model_id=booking_id)
    assert booking is None
