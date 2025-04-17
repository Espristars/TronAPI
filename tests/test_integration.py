import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from tronpy.keys import is_base58check_address


@pytest.mark.asyncio
async def test_post_wallet():
    payload = {"address": "TNMcQVGPzqH9ZfMCSY4PNrukevtDgp24dK"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/wallet", json=payload)

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["address"] == payload["address"]
    assert "bandwidth" in data and "energy" in data and "balance_trx" in data
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_post_wallet_invalid_address():
    payload = {"address": "INVALID_TRON_ADDRESS"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/wallet", json=payload)

    assert response.status_code == 400
    assert "Невалидный TRON-адрес" in response.text
