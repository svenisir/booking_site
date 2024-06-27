import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    *[(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)],
    (4, "2030-04-30", "2030-05-10", 10, 409),
    (4, "2030-05-07", "2030-05-12", 10, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms,
                                   status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")

    assert len(response.json()) == booked_rooms


async def test_get_and_delete_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")

    assert response.status_code == 200

    bookings = response.json()
    for booking in bookings:
        print(booking)
        # response = await authenticated_ac.get(f"/bookings/{booking['id']}", params={
        #     "booking_id": booking['id']
        # })

        assert response.status_code == 204
