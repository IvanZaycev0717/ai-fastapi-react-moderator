import pytest
from httpx import ASGITransport, AsyncClient

from main import app

pytestmark = pytest.mark.asyncio


async def test_main_api():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as ac:
        response = await ac.get("/comments/")
    print(response.content)
    assert response.status_code == 200
