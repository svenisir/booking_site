from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsExceptions(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен не существует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotGetException(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UserRoleException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных комнат"


class HotelIsNotExistException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND


class BookingsIsNotExistForThisUserException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "У вас нет такой брони"


class BookingIsDeleteException(BookingException):
    status_code = status.HTTP_204_NO_CONTENT
    detail = "Бронь успешно удалена" 


class DateToGradeThenDateFromException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда позже даты выезда"


class InvalidBookingTimeException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Разница между датой заезда и датой выезда более 30 дней"
