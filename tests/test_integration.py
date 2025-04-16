import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app

@pytest.mark.asyncio
async def test_post_wallet():
    payload = {"address": "TVMjr6X2p6WJd1yZrY84UipQAY8nq9vPqg"}

    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/wallet", json=payload)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["address"] == payload["address"]
    assert "bandwidth" in data and "energy" in data and "balance_trx" in data
    assert "timestamp" in data
