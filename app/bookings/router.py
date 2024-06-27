from datetime import date, timedelta
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingForUser, SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exeptions import RoomCannotBeBooked, BookingsIsNotExistForThisUserException, \
    BookingIsDeleteException, DateToGradeThenDateFromException, InvalidBookingTimeException
from app.tasks.tasks import send_booking_confirmation_email

from fastapi import APIRouter, Depends, Response
from pydantic import parse_obj_as

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingForUser]:
    return await BookingDAO.find_all_by_user_id(user_id=user.id)


@router.post("")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_current_user),
) -> SBooking:
    if date_from >= date_to:
        raise DateToGradeThenDateFromException
    elif date_to - date_from > timedelta(days=30):
        raise InvalidBookingTimeException

    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCannotBeBooked

    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(
        response: Response,
        booking_id: int,
        user: Users = Depends(get_current_user)
) -> None:
    bookings = await BookingDAO.find_all(user_id=user.id)
    if any([booking["id"] == booking_id for booking in bookings]):
        response.status_code = BookingIsDeleteException.status_code
        await BookingDAO.delete_by_id(model_id=booking_id)
    else:
        raise BookingsIsNotExistForThisUserException
