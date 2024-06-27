from datetime import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location,date_from,date_to,status_code", [
    ("Алтай", "2027-05-01", "2027-05-14", 200),
    ("Алтай", "2027-05-14", "2027-05-01", 400),
    ("Алтай", "2027-05-01", "2027-06-14", 400),

])
async def test_get_hotels(location, date_from, date_to, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/{location}", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code
