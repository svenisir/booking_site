import csv
import codecs

from fastapi import APIRouter, UploadFile, Depends
from pydantic import parse_obj_as, ValidationError

from app.users.models import Users
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.bookings.dao import BookingDAO
from app.users.dependencies import get_current_user
from app.importer.enums import TablesEnum
from app.importer.schemas import SHotelsCSV, SBookingCSV, SRoomCSV
from app.exeptions import InvalidDataFormatException

router = APIRouter(
    prefix="/import",
    tags=["Добавление из файла"]
)


@router.post("/hotels")
async def add_hotels_or_rooms_or_bookings_from_file(
        table_name: TablesEnum,
        file: UploadFile,
        user: Users = Depends(get_current_user)
):
    data = csv.DictReader(codecs.iterdecode(file.file, "utf-8"), delimiter=';')

    async def add_data_in_table(TableDAO, SchemasCSV):
        for row in data:
            try:
                row = parse_obj_as(SchemasCSV, row).dict()
            except ValidationError:
                raise InvalidDataFormatException

            await TableDAO.add(**row)

    if table_name == TablesEnum.hotels:
        await add_data_in_table(HotelDAO, SHotelsCSV)
    elif table_name == TablesEnum.bookings:
        await add_data_in_table(BookingDAO, SBookingCSV)
    elif table_name == TablesEnum.rooms:
        await add_data_in_table(RoomDAO, SRoomCSV) 

    file.file.close()
