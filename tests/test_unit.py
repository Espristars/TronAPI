import pytest
from datetime import datetime
from models import WalletRequest, AsyncSessionLocal

@pytest.mark.asyncio
async def test_db_write():
    wallet_address = "TNMcQVGPzqH9ZfMCSY4PNrukevtDgp24dK"
    async with AsyncSessionLocal() as session:
        record = WalletRequest(
            wallet=wallet_address,
            bandwidth=1200,
            energy=600,
            balance_trx=1234.56,
            created_at=datetime.now()
        )
        session.add(record)
        await session.commit()
        await session.refresh(record)
        assert record.id is not None
        assert record.wallet == wallet_address

        result = await session.execute(
            WalletRequest.__table__.select().where(WalletRequest.wallet == wallet_address)
        )
        fetched = result.first()
        assert fetched is not None
        assert fetched.wallet == wallet_address
