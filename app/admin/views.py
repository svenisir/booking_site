from sqladmin import ModelView
from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.booking]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_details_exclude_list = ["hashed_password", "role"]


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.columns] + [Bookings.user, Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.columns] + [Rooms.hotel, Rooms.booking]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.columns] + [Hotels.room]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
