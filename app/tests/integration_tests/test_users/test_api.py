from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email,password,status_code", [
    ("dog@cat.com", "password", 200),
    ("dog@cat.com", "password", 409),
    ("cat@cat.com", "password", 200),
    ("catcat.com", "password", 422),
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("test@test.com", "test", 200),
    ("artem@example.com", "artem", 200),
    ("aaaa@eeeee.com", "aaaeee", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code

